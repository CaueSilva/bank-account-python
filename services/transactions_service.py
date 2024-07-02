from _decimal import Decimal
from werkzeug.exceptions import NotFound
from repository.transactions_repository import TransactionsRepository
from util.enums.account_status import Status
from util.enums.transactions_types import TransactionsTypes
from util.validator import Validator
from util.schemas_templates import account_financial_operation_schema, transfer_schema
from exceptions.exceptions import AccountNotFound, InsufficientBalance, StatusNotAllowed, TransactionNotFound
from sqlalchemy.exc import NoResultFound
from services.accounts_service import AccountsService
from builders.transaction_builder import TransactionBuilder
from util.params_utils import ParamsUtils as param_utils


class TransactionsService:

    def __init__(self):
        self.__transactions_repository = TransactionsRepository()
        self.__validator = Validator()
        self.__accounts_service = AccountsService()
        self.__transaction_builder = TransactionBuilder()

    def deposit(self, body):
        try:
            self.__validator.validate_body(body, account_financial_operation_schema)
            account = self.__accounts_service.get_account_by_id(body['account_id'], False)
            if self.__account_is_active(account):
                self.__accounts_service.update_account(account, Decimal(body['value']).quantize(Decimal('1.00')))
                transaction = self.__transactions_repository.create_transaction(
                    self.__transaction_builder.transaction_builder(body, TransactionsTypes.DEPOSIT.value, body['account_id'])
                )
                return {
                    'message': 'Deposit made successfully!',
                    'transaction': {
                        'transaction_id': transaction.transaction_id,
                        'transaction_type': transaction.transaction_type,
                        'transaction_value': str(Decimal(transaction.transaction_value).quantize(Decimal('1.00'))),
                        'transaction_date': transaction.transaction_date.strftime("%Y-%m-%dT%H:%M:%S"),
                        'account_id': transaction.origin_account
                    }
                }
            raise StatusNotAllowed('Account is not active.')
        except NoResultFound:
            raise AccountNotFound('Account not found.')

    def withdraw(self, body):
        try:
            self.__validator.validate_body(body, account_financial_operation_schema)
            account = self.__accounts_service.get_account_by_id(body['account_id'], False)
            if self.__account_is_active(account):
                self.__account_balance_is_valid(account, body['value'])
                self.__accounts_service.update_account(account, Decimal(body['value'] * -1).quantize(Decimal('1.00')))
                transaction = self.__transactions_repository.create_transaction(
                    self.__transaction_builder.transaction_builder(body, TransactionsTypes.WITHDRAW.value, body['account_id'])
                )
                return {
                    'message': 'Withdraw made successfully!',
                    'transaction': {
                        'transaction_id': transaction.transaction_id,
                        'transaction_type': transaction.transaction_type,
                        'transaction_value': str(Decimal(transaction.transaction_value).quantize(Decimal('1.00'))),
                        'transaction_date': transaction.transaction_date.strftime("%Y-%m-%dT%H:%M:%S"),
                        'account_id': transaction.origin_account
                    }
                }
            raise StatusNotAllowed('Account is not active.')
        except NoResultFound:
            raise AccountNotFound('Account not found.')

    @staticmethod
    def __account_balance_is_valid(account, value):
        if value > account.balance:
            raise InsufficientBalance("Account doesn't have enough balance to complete operation.")

    @staticmethod
    def __account_is_active(account):
        return account.status == Status.ACTIVE.value

    def transfer(self, body):
        self.__validator.validate_body(body, transfer_schema)
        origin_account = self.__accounts_service.get_account_by_id(body['original_account_id'], False)
        destination_account = self.__accounts_service.get_account_by_id(body['destination_account_id'], False)
        transaction_value = Decimal(body['value'])
        self.__validate_transfer_accounts(origin_account, destination_account, transaction_value)
        self.__accounts_service.update_account(origin_account, Decimal(transaction_value * -1).quantize(Decimal('1.00')))
        self.__accounts_service.update_account(destination_account, Decimal(transaction_value).quantize(Decimal('1.00')))
        transaction = self.__transactions_repository.create_transaction(
            self.__transaction_builder.transaction_builder(body, TransactionsTypes.TRANSFER.value)
        )
        return {
            'message': 'Transfer completed with success.',
            'transaction': {
                'transaction_id': transaction.transaction_id,
                'transaction_type': transaction.transaction_type,
                'transaction_value': str(Decimal(transaction.transaction_value).quantize(Decimal('1.00'))),
                'transaction_date': transaction.transaction_date.strftime("%Y-%m-%dT%H:%M:%S"),
                'origin_account': transaction.origin_account,
                'destination_account': transaction.destination_account
            }
        }

    def __validate_transfer_accounts(self, origin_account, destination_account, value):
        if not self.__account_is_active(origin_account):
            raise StatusNotAllowed('Origin Account is not active.')
        if not self.__account_is_active(destination_account):
            raise StatusNotAllowed('Destination Account is not active.')
        if value > origin_account.balance:
            raise InsufficientBalance("Origin Account doesn't have enough balance to complete operation.")

    def get_all_transactions(self, headers):
        try:
            self.__validator.validate_params(headers, ['currentPage', 'maxItemsPerPage'])
            params = param_utils.update_params({'currentPage': 1, 'maxItemsPerPage': 50}, headers.environ['QUERY_STRING'])
            transactions = sorted(self.__transactions_repository.get_transactions(params), key=lambda transaction: transaction.transaction_date)
            return {
                'currentPage': params['currentPage'],
                'maxItemsPerPage': params['maxItemsPerPage'],
                'transactions': [
                    {
                        'transaction_id': transaction.transaction_id,
                        'transaction_type': TransactionsTypes(transaction.transaction_type).name,
                        'transaction_value': str(Decimal(transaction.transaction_value).quantize(Decimal('1.00'))),
                        'transaction_date': transaction.transaction_date.strftime("%Y-%m-%dT%H:%M:%S"),
                        'origin_account': transaction.origin_account,
                        'destination_account': '' if not transaction.destination_account else transaction.destination_account
                    } for transaction in transactions
                ]
            }
        except NotFound:
            raise TransactionNotFound('No transactions found.')

    def get_transaction_by_id(self, transaction_id):
        try:
            transaction = self.__transactions_repository.get_transaction_by_id(transaction_id)
            return {
                'transaction_id': transaction.transaction_id,
                'transaction_type': TransactionsTypes(transaction.transaction_type).name,
                'transaction_value': str(Decimal(transaction.transaction_value).quantize(Decimal('1.00'))),
                'transaction_date': transaction.transaction_date.strftime("%Y-%m-%dT%H:%M:%S"),
                'origin_account': transaction.origin_account,
                'destination_account': '' if not transaction.destination_account else transaction.destination_account
            }
        except NoResultFound:
            raise TransactionNotFound('Transaction not found.')
