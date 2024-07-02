from sqlalchemy import text
from models.HolderModel import HolderModel
from config.db_config import session


class HoldersRepository:

    select_statement = 'SELECT * FROM holders.holders'

    def get_holders(self, params):
        try:
            return HolderModel.query.paginate(page=params['currentPage'], per_page=params['maxItemsPerPage'], error_out=True)
        except Exception as e:
            raise e

    def get_holder_by_id(self, holder_id):
        try:
            stmt = text(self.select_statement + f' WHERE holder_id = {holder_id}')
            return session.query(HolderModel).from_statement(stmt).one()
        except Exception as e:
            raise e

    def get_holder_by_document(self, holder_document):
        try:
            stmt = text(self.select_statement + ' WHERE document = \'{}\''.format(holder_document))
            return session.query(HolderModel).from_statement(stmt).all()
        except Exception as e:
            raise e

    def create_holder(self, holder):
        try:
            session.add(holder)
            session.commit()
            return holder
        except Exception as e:
            raise e

    def update_holder(self):
        try:
            session.commit()
        except Exception as e:
            raise e
