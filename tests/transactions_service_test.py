from decimal import Decimal
from unittest import TestCase
from unittest.mock import patch
from jsonschema.exceptions import ValidationError
from sqlalchemy.exc import NoResultFound
from werkzeug.datastructures import EnvironHeaders
from werkzeug.exceptions import NotFound

from exceptions.exceptions import AccountNotFound, InsufficientBalance, StatusNotAllowed, TransactionNotFound
from services.transactions_service import TransactionsService
from builders.transaction_builder import TransactionBuilder
from util.enums.transactions_types import TransactionsTypes
from builder import return_financial_operation_body, return_active_account, return_financial_operation, \
    return_transfer_body, return_transfer_operation, return_blocked_account, return_closed_account, \
    return_list_of_transactions


class TransactionsServiceTest(TestCase):

    transactions_service = TransactionsService()
    transaction_builder = TransactionBuilder()
    default_current_page = 1
    default_max_items_per_page = 50

    @staticmethod
    def successful_transfer_side_effect(*args, **kwargs):
        if args[0] == 1:
            account = return_active_account()
            account.account_id = 1
            account.balance = Decimal('200').quantize(Decimal('1.00'))
            return account
        else:
            account = return_active_account()
            account.account_id = 2
            return account

    @staticmethod
    def insufficient_balance_origin_account_side_effect(*args, **kwargs):
        if args[0] == 1:
            account = return_active_account()
            account.account_id = 1
            account.balance = Decimal('0')
            return account
        else:
            account = return_active_account()
            account.account_id = 2
            return account

    @staticmethod
    def origin_account_blocked_side_effect(*args, **kwargs):
        if args[0] == 1:
            account = return_blocked_account()
            account.account_id = 1
            return account
        else:
            account = return_active_account()
            account.account_id = 2
            return account

    @staticmethod
    def destination_account_blocked_side_effect(*args, **kwargs):
        if args[0] == 1:
            account = return_active_account()
            account.account_id = 1
            return account
        else:
            account = return_blocked_account()
            account.account_id = 2
            return account

    @patch('repository.transactions_repository.TransactionsRepository.create_transaction')
    @patch('repository.accounts_repository.AccountsRepository.update_account')
    @patch('repository.accounts_repository.AccountsRepository.get_account_by_account_id')
    def test_deposit_made_successfully(self,
                                       get_account_by_account_id_mock,
                                       update_account_mock,
                                       create_transaction_mock):
        get_account_by_account_id_mock.return_value = return_active_account()
        create_transaction_mock.return_value = return_financial_operation(TransactionsTypes.DEPOSIT.value)

        result = self.transactions_service.deposit(return_financial_operation_body())

        self.assertEqual('Deposit made successfully!', result['message'])

    @patch('repository.transactions_repository.TransactionsRepository.create_transaction')
    @patch('repository.accounts_repository.AccountsRepository.update_account')
    @patch('repository.accounts_repository.AccountsRepository.get_account_by_account_id')
    def test_withdraw_made_successfully(self,
                                        get_account_by_account_id_mock,
                                        update_account_mock,
                                        create_transaction_mock):
        account = return_active_account()
        account.balance = Decimal('200').quantize(Decimal('1.00'))
        get_account_by_account_id_mock.return_value = account
        create_transaction_mock.return_value = return_financial_operation(TransactionsTypes.DEPOSIT.value)

        result = self.transactions_service.withdraw(return_financial_operation_body())

        self.assertEqual('Withdraw made successfully!', result['message'])

    @patch('repository.transactions_repository.TransactionsRepository.create_transaction')
    @patch('repository.accounts_repository.AccountsRepository.update_account')
    @patch('repository.accounts_repository.AccountsRepository.get_account_by_account_id')
    def test_transfer_made_successfully(self,
                                        get_account_by_account_id_mock,
                                        update_account_mock,
                                        create_transaction_mock):
        get_account_by_account_id_mock.side_effect = self.successful_transfer_side_effect
        create_transaction_mock.return_value = return_transfer_operation()

        result = self.transactions_service.transfer(return_transfer_body())

        self.assertEqual('Transfer completed with success.', result['message'])

    def test_account_transaction_raised_validation_error(self):
        body = return_financial_operation_body()
        body['value'] = 0

        with self.assertRaises(ValidationError) as exception_result:
            self.transactions_service.deposit(body)

        self.assertEqual('{} is less than the minimum of 0.01'.format(body['value']),
                         exception_result.exception.args[0])

        body['value'] = "100"

        with self.assertRaises(ValidationError) as exception_result:
            self.transactions_service.deposit(body)

        self.assertEqual('\'{}\' is not of type \'number\''.format(body['value']),
                         exception_result.exception.args[0])

    @patch('repository.accounts_repository.AccountsRepository.get_account_by_account_id')
    def test_transaction_raised_error_when_account_is_not_found(self,
                                                                get_account_by_account_id_mock):
        get_account_by_account_id_mock.side_effect = NoResultFound()

        with self.assertRaises(AccountNotFound) as exception_result:
            self.transactions_service.deposit(return_financial_operation_body())

        self.assertEqual('Account not found.', exception_result.exception.args[0])

        with self.assertRaises(AccountNotFound) as exception_result:
            self.transactions_service.withdraw(return_financial_operation_body())

        self.assertEqual('Account not found.', exception_result.exception.args[0])

    @patch('repository.accounts_repository.AccountsRepository.get_account_by_account_id')
    def test_withdraw_returned_insufficient_balance(self,
                                                    get_account_by_account_id_mock):
        account = return_active_account()
        account.balance = Decimal('0')

        get_account_by_account_id_mock.return_value = account

        with self.assertRaises(InsufficientBalance) as exception_result:
            self.transactions_service.withdraw(return_financial_operation_body())

        self.assertEqual("Account doesn't have enough balance to complete operation.", exception_result.exception.args[0])

    @patch('repository.transactions_repository.TransactionsRepository.create_transaction')
    @patch('repository.accounts_repository.AccountsRepository.get_account_by_account_id')
    def test_transfer_returned_insufficient_balance(self,
                                                    get_account_by_account_id_mock,
                                                    create_transaction_mock):
        get_account_by_account_id_mock.side_effect = self.insufficient_balance_origin_account_side_effect
        body = return_transfer_body()
        create_transaction_mock.return_value = return_transfer_operation(body)

        with self.assertRaises(InsufficientBalance) as exception_result:
            self.transactions_service.transfer(body)

        self.assertEqual("Origin Account doesn't have enough balance to complete operation.", exception_result.exception.args[0])

    @patch('repository.accounts_repository.AccountsRepository.get_account_by_account_id')
    def test_transaction_returned_account_not_active(self,
                                                     get_account_by_account_id_mock):
        get_account_by_account_id_mock.return_value = return_blocked_account()

        with self.assertRaises(StatusNotAllowed) as exception_result:
            self.transactions_service.deposit(return_financial_operation_body())

        self.assertEqual('Account is not active.', exception_result.exception.args[0])

        with self.assertRaises(StatusNotAllowed) as exception_result:
            self.transactions_service.withdraw(return_financial_operation_body())

        self.assertEqual('Account is not active.', exception_result.exception.args[0])

        get_account_by_account_id_mock.return_value = return_closed_account()

        with self.assertRaises(StatusNotAllowed) as exception_result:
            self.transactions_service.deposit(return_financial_operation_body())

        self.assertEqual('Account is not active.', exception_result.exception.args[0])

        with self.assertRaises(StatusNotAllowed) as exception_result:
            self.transactions_service.withdraw(return_financial_operation_body())

        self.assertEqual('Account is not active.', exception_result.exception.args[0])

    @patch('repository.accounts_repository.AccountsRepository.get_account_by_account_id')
    def test_transfer_returned_account_not_active(self,
                                                  get_account_by_account_id_mock):
        get_account_by_account_id_mock.side_effect = self.origin_account_blocked_side_effect

        with self.assertRaises(StatusNotAllowed) as exception_result:
            self.transactions_service.transfer(return_transfer_body())

        self.assertEqual('Origin Account is not active.', exception_result.exception.args[0])

        get_account_by_account_id_mock.side_effect = self.destination_account_blocked_side_effect

        with self.assertRaises(StatusNotAllowed) as exception_result:
            self.transactions_service.transfer(return_transfer_body())

        self.assertEqual('Destination Account is not active.', exception_result.exception.args[0])

    @patch('repository.transactions_repository.TransactionsRepository.get_transactions')
    def test_get_transactions_was_found_successfully(self,
                                                     get_transactions_mock):

        get_transactions_mock.return_value = return_list_of_transactions()
        headers = EnvironHeaders({"QUERY_STRING": ''})
        result = self.transactions_service.get_all_transactions(headers)

        self.assertEqual(self.default_current_page, result['currentPage'])
        self.assertEqual(self.default_max_items_per_page, result['maxItemsPerPage'])
        self.assertEqual(2, len(result['transactions']))

    @patch('repository.transactions_repository.TransactionsRepository.get_transactions')
    def test_get_transactions_raised_not_found(self,
                                               get_transactions_mock):
        get_transactions_mock.side_effect = NotFound()
        headers = EnvironHeaders({"QUERY_STRING": ''})

        with self.assertRaises(TransactionNotFound) as exception_result:
            self.transactions_service.get_all_transactions(headers)

        self.assertEqual('No transactions found.', exception_result.exception.args[0])

    @patch('repository.transactions_repository.TransactionsRepository.get_transaction_by_id')
    def test_get_transaction_by_id_found_successfully(self,
                                                      get_transaction_by_id_mock):
        get_transaction_by_id_mock.return_value = return_transfer_operation()

        result = self.transactions_service.get_transaction_by_id('')

        self.assertTrue(result)

    @patch('repository.transactions_repository.TransactionsRepository.get_transaction_by_id')
    def test_get_transaction_by_id_raised_not_found(self,
                                                    get_transaction_by_id_mock):
        get_transaction_by_id_mock.side_effect = NoResultFound()

        with self.assertRaises(TransactionNotFound) as exception_result:
            result = self.transactions_service.get_transaction_by_id('')

        self.assertEqual('Transaction not found.', exception_result.exception.args[0])
