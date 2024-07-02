from config.db_config import session
from models.TransactionModel import TransactionModel
from sqlalchemy import text


class TransactionsRepository:

    select_statement = 'SELECT * FROM accounts.transactions'

    def create_transaction(self, transaction):
        try:
            session.add(transaction)
            session.commit()
            return transaction
        except Exception as e:
            raise e

    def get_transactions(self, params):
        try:
            return TransactionModel.query.paginate(page=params['currentPage'], per_page=params['maxItemsPerPage'], error_out=True)
        except Exception as e:
            raise e

    def get_transaction_by_id(self, transaction_id):
        try:
            stmt = text(self.select_statement + f' WHERE transaction_id = \'{transaction_id}\'')
            return session.query(TransactionModel).from_statement(stmt).one()
        except Exception as e:
            raise e
