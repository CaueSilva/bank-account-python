from sqlalchemy import text
from models.AccountModel import AccountModel
from config.db_config import session


class AccountsRepository:

    select_statement = 'SELECT * FROM accounts.accounts'

    def create_account(self, account):
        try:
            session.add(account)
            session.commit()
            return account
        except Exception as e:
            raise e

    def get_accounts(self, params):
        try:
            return AccountModel.query.paginate(page=params['currentPage'], per_page=params['maxItemsPerPage'], error_out=True)
        except Exception as e:
            raise e

    def get_account_by_account_id(self, account_id):
        try:
            stmt = text(self.select_statement + f' WHERE account_id = {account_id}')
            return session.query(AccountModel).from_statement(stmt).one()
        except Exception as e:
            raise e

    def update_account(self):
        try:
            session.commit()
        except Exception as e:
            raise e

    def get_accounts_by_holder_id(self, holder_id):
        try:
            stmt = text(self.select_statement + f' WHERE holder_id = {holder_id}')
            return session.query(AccountModel).from_statement(stmt).all()
        except Exception as e:
            raise e
