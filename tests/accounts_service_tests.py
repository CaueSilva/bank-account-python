from decimal import Decimal
from unittest import TestCase
from unittest.mock import patch

from jsonschema.exceptions import ValidationError
from sqlalchemy.exc import NoResultFound

from werkzeug.datastructures.headers import EnvironHeaders
from werkzeug.exceptions import NotFound

from builders.account_builder import AccountBuilder
from builder import return_account_creation_body, return_active_account, \
    return_blocked_account, return_closed_account, return_list_of_accounts
from exceptions.exceptions import HolderNotFound, AccountAlreadyExistentByHolder, StatusNotAllowed, AccountNotFound
from services.accounts_service import AccountsService
from util.enums.account_status import Status


class AccountsServiceTest(TestCase):
    accounts_service = AccountsService()
    account_builder = AccountBuilder()
    default_current_page = 1
    default_max_items_per_page = 50

    @patch('repository.accounts_repository.AccountsRepository.create_account')
    @patch('repository.accounts_repository.AccountsRepository.get_accounts_by_holder_id')
    @patch('repository.holders_repository.HoldersRepository.get_holder_by_id')
    def test_account_created_with_success(self,
                                          get_holder_by_id_mock,
                                          get_accounts_by_holder_id_mock,
                                          create_account_mock):
        get_accounts_by_holder_id_mock.return_value = []
        account = self.account_builder.account_builder(1)
        create_account_mock.return_value = account
        account.account_id = 1

        result = self.accounts_service.create_account(return_account_creation_body())

        self.assertEqual('Account created with success!', result['message'])
        self.assertEqual(account.account_id, int(result['account']['account_id']))
        self.assertEqual(Decimal(account.balance).quantize(Decimal('1.00')),
                         Decimal(result['account']['balance']).quantize(Decimal('1.00')))
        self.assertEqual(Status.ACTIVE.name, result['account']['status'])

    def test_account_creation_returned_validation_error(self):
        body = return_account_creation_body()
        body['holder_id'] = "14"
        with self.assertRaises(ValidationError) as exception_result:
            self.accounts_service.create_account(body)

        self.assertEqual('\'{}\' is not of type \'number\''.format(body['holder_id']),
                         exception_result.exception.args[0])

        body['holder_id'] = -1
        with self.assertRaises(ValidationError) as exception_result:
            self.accounts_service.create_account(body)

        self.assertEqual('{} is less than the minimum of 1'.format(body['holder_id']),
                         exception_result.exception.args[0])

        body['holder_id'] = 0.01
        with self.assertRaises(ValidationError) as exception_result:
            self.accounts_service.create_account(body)

        self.assertEqual('{} is less than the minimum of 1'.format(body['holder_id']),
                         exception_result.exception.args[0])

    @patch('repository.holders_repository.HoldersRepository.get_holder_by_id')
    def test_account_creation_raised_error_when_holder_is_not_found(self,
                                                                    get_holder_by_id_mock):
        get_holder_by_id_mock.side_effect = NoResultFound()

        with self.assertRaises(HolderNotFound) as exception_result:
            self.accounts_service.create_account(return_account_creation_body())

        self.assertEqual('Holder not found.', exception_result.exception.args[0])

    @patch('repository.accounts_repository.AccountsRepository.get_accounts_by_holder_id')
    @patch('repository.holders_repository.HoldersRepository.get_holder_by_id')
    def test_account_creation_raised_error_when_holder_already_have_a_non_closed_account(self,
                                                                                         get_holder_by_id_mock,
                                                                                         get_accounts_by_holder_id_mock):
        get_accounts_by_holder_id_mock.return_value = [return_active_account()]

        with self.assertRaises(AccountAlreadyExistentByHolder) as exception_result:
            self.accounts_service.create_account(return_account_creation_body())

        self.assertEqual('Holder already have an Account.', exception_result.exception.args[0])

        get_accounts_by_holder_id_mock.return_value = [return_blocked_account()]

        with self.assertRaises(AccountAlreadyExistentByHolder) as exception_result:
            self.accounts_service.create_account(return_account_creation_body())

        self.assertEqual('Holder already have an Account.', exception_result.exception.args[0])

    @patch('repository.accounts_repository.AccountsRepository.update_account')
    @patch('repository.accounts_repository.AccountsRepository.get_account_by_account_id')
    def test_account_block_with_success(self,
                                        get_account_by_account_id_mock,
                                        update_account_mock):
        get_account_by_account_id_mock.return_value = return_active_account()

        result = self.accounts_service.block_account(1)

        self.assertEqual('Account blocked.', result['message'])
        self.assertEqual(Status.BLOCKED.name, result['account']['status'])

    @patch('repository.accounts_repository.AccountsRepository.update_account')
    @patch('repository.accounts_repository.AccountsRepository.get_account_by_account_id')
    def test_account_close_with_success(self,
                                        get_account_by_account_id_mock,
                                        update_account_mock):
        get_account_by_account_id_mock.return_value = return_active_account()

        result = self.accounts_service.close_account(1)

        self.assertEqual('Account closed.', result['message'])
        self.assertEqual(Status.CLOSED.name, result['account']['status'])

        get_account_by_account_id_mock.return_value = return_blocked_account()

        result = self.accounts_service.close_account(1)

        self.assertEqual('Account closed.', result['message'])
        self.assertEqual(Status.CLOSED.name, result['account']['status'])

    @patch('repository.accounts_repository.AccountsRepository.update_account')
    @patch('repository.accounts_repository.AccountsRepository.get_account_by_account_id')
    def test_account_reactivate_with_success(self,
                                             get_account_by_account_id_mock,
                                             update_account_mock):
        get_account_by_account_id_mock.return_value = return_blocked_account()

        result = self.accounts_service.reactivate_account(1)

        self.assertEqual('Account reactivated.', result['message'])
        self.assertEqual(Status.ACTIVE.name, result['account']['status'])

    @patch('repository.accounts_repository.AccountsRepository.get_account_by_account_id')
    def test_account_change_status_raised_error_when_account_is_already_closed(self,
                                                                               get_account_by_account_id_mock):
        get_account_by_account_id_mock.return_value = return_closed_account()

        with self.assertRaises(StatusNotAllowed) as exception_result:
            self.accounts_service.block_account(1)

        self.assertEqual('Account is already closed.', exception_result.exception.args[0])

        with self.assertRaises(StatusNotAllowed) as exception_result:
            self.accounts_service.reactivate_account(1)

        self.assertEqual('Account is already closed.', exception_result.exception.args[0])

        with self.assertRaises(StatusNotAllowed) as exception_result:
            self.accounts_service.close_account(1)

        self.assertEqual('Account is already closed.', exception_result.exception.args[0])

    @patch('repository.accounts_repository.AccountsRepository.get_account_by_account_id')
    def test_account_change_status_raised_error_when_account_is_not_found(self,
                                                                          get_account_by_account_id_mock):
        get_account_by_account_id_mock.side_effect = NoResultFound()

        with self.assertRaises(AccountNotFound) as exception_result:
            self.accounts_service.reactivate_account(1)

        self.assertEqual('Account not found.', exception_result.exception.args[0])

        with self.assertRaises(AccountNotFound) as exception_result:
            self.accounts_service.block_account(1)

        self.assertEqual('Account not found.', exception_result.exception.args[0])

        with self.assertRaises(AccountNotFound) as exception_result:
            self.accounts_service.close_account(1)

        self.assertEqual('Account not found.', exception_result.exception.args[0])

    @patch('repository.accounts_repository.AccountsRepository.get_account_by_account_id')
    def test_get_account_by_id_return_with_success(self,
                                                   get_account_by_account_id_mock):
        get_account_by_account_id_mock.return_value = return_active_account()

        result = self.accounts_service.get_account_by_id(1)

        self.assertTrue(result)

    @patch('repository.accounts_repository.AccountsRepository.get_account_by_account_id')
    def test_get_account_by_id_raised_not_found_error(self,
                                                      get_account_by_account_id_mock):
        get_account_by_account_id_mock.side_effect = NoResultFound()

        with self.assertRaises(AccountNotFound) as exception_result:
            self.accounts_service.get_account_by_id(1)

        self.assertEqual('Account not found.', exception_result.exception.args[0])

    @patch('repository.accounts_repository.AccountsRepository.get_accounts')
    def test_get_all_accounts_returned_with_success(self,
                                                    get_accounts_mock):
        get_accounts_mock.return_value = return_list_of_accounts()
        headers = EnvironHeaders({"QUERY_STRING": ''})
        result = self.accounts_service.get_all_accounts(headers)

        self.assertEqual(self.default_current_page, result['currentPage'])
        self.assertEqual(self.default_max_items_per_page, result['maxItemsPerPage'])
        self.assertEqual(2, len(result['accounts']))

    @patch('repository.accounts_repository.AccountsRepository.get_accounts')
    def test_get_all_accounts_raised_not_found_error(self,
                                                     get_accounts_mock):
        get_accounts_mock.side_effect = NotFound()
        headers = EnvironHeaders({"QUERY_STRING": ''})

        with self.assertRaises(AccountNotFound) as exception_result:
            self.accounts_service.get_all_accounts(headers)

        self.assertEqual('No accounts found.', exception_result.exception.args[0])

