from werkzeug.exceptions import NotFound

from util.validator import Validator
from util.schemas_templates import post_account_schema
from services.holders_service import HoldersService
from builders.account_builder import AccountBuilder
from repository.accounts_repository import AccountsRepository
from util.enums.account_status import Status
from util.params_utils import ParamsUtils as param_utils
from sqlalchemy.exc import NoResultFound
from exceptions.exceptions import AccountNotFound, StatusNotAllowed, AccountAlreadyExistentByHolder


class AccountsService:

    def __init__(self):
        self.__validator = Validator()
        self.__holders_service = HoldersService()
        self.__account_builder = AccountBuilder()
        self.__account_repository = AccountsRepository()

    def create_account(self, body):
        self.__validator.validate_body(body, post_account_schema)
        holder_id = body['holder_id']
        self.__holders_service.get_holder_by_id(holder_id)
        if self.__holder_have_account_not_closed(holder_id):
            raise AccountAlreadyExistentByHolder('Holder already have an Account.')
        account = self.__account_repository.create_account(self.__account_builder.account_builder(holder_id))
        return {
            'message': 'Account created with success!',
            'account': {
                'account_id': account.account_id,
                'holder_id': account.holder_id,
                'balance': str(account.balance),
                'status': Status.ACTIVE.name
            }
        }

    def __holder_have_account_not_closed(self, holder_id):
        accounts = self.__account_repository.get_accounts_by_holder_id(holder_id)
        return any(account.status != Status.CLOSED.value for account in accounts)

    def get_account_by_id(self, account_id, return_dict=True):
        try:
            account = self.__account_repository.get_account_by_account_id(account_id)
            if return_dict:
                return {
                    'account_id': account.account_id,
                    'holder_id': account.holder_id,
                    'balance': str(account.balance),
                    'status': Status(account.status).name
                }
            return account
        except NoResultFound:
            raise AccountNotFound('Account not found.')

    def get_all_accounts(self, headers):
        try:
            self.__validator.validate_params(headers, ['currentPage', 'maxItemsPerPage'])
            params = param_utils.update_params({'currentPage': 1, 'maxItemsPerPage': 50}, headers.environ['QUERY_STRING'])
            accounts = sorted(self.__account_repository.get_accounts(params), key=lambda account: account.account_id)
            return {
                'currentPage': params['currentPage'],
                'maxItemsPerPage': params['maxItemsPerPage'],
                'accounts': [
                    {
                        'account_id': account.account_id,
                        'holder_id': account.holder_id,
                        'balance': str(account.balance),
                        'status': Status(account.status).name
                    } for account in accounts
                ]
            }
        except NotFound:
            raise AccountNotFound('No accounts found.')

    def block_account(self, account_id):
        try:
            account = self.__change_account_status(account_id, Status.BLOCKED.value)
            return self.__return_status_message(account)
        except NoResultFound:
            raise AccountNotFound('Account not found.')

    def reactivate_account(self, account_id):
        try:
            account = self.__change_account_status(account_id, Status.ACTIVE.value)
            return self.__return_status_message(account)
        except NoResultFound:
            raise AccountNotFound('Account not found.')

    def close_account(self, account_id):
        try:
            account = self.__change_account_status(account_id, Status.CLOSED.value)
            return self.__return_status_message(account)
        except NoResultFound:
            raise AccountNotFound('Account not found.')

    def __change_account_status(self, account_id, status):
        account = self.__account_repository.get_account_by_account_id(account_id)
        if self.__is_account_closed(account):
            raise StatusNotAllowed('Account is already closed.')
        account.status = status
        self.__account_repository.update_account()
        return account

    @staticmethod
    def __return_status_message(account):
        message = 'Account blocked.' if account.status == Status.BLOCKED.value else \
            'Account reactivated.' if account.status == Status.ACTIVE.value else \
            'Account closed.'
        return {
            'message': message,
            'account': {
                'account_id': account.account_id,
                'holder_id': account.holder_id,
                'balance': str(account.balance),
                'status': Status(account.status).name
            }
        }

    @staticmethod
    def __is_account_closed(account):
        return account.status == Status.CLOSED.value

    def update_account(self, account, value):
        account.balance += value
        self.__account_repository.update_account()
