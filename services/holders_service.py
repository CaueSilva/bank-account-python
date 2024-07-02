from sqlalchemy.exc import NoResultFound
from werkzeug.exceptions import NotFound
from repository.holders_repository import HoldersRepository
from util.schemas_templates import post_holder_schema, put_holder_schema
from util.validator import Validator
from builders.holder_builder import HolderBuilder
from exceptions.exceptions import DocumentAlreadyExists, HolderNotFound
from util.params_utils import ParamsUtils as params_utils


class HoldersService:

    def __init__(self):
        self.__holders_repository = HoldersRepository()
        self.__validator = Validator()
        self.__holder_builder = HolderBuilder()

    def get_all_holders(self, headers):
        try:
            self.__validator.validate_params(headers, ['currentPage', 'maxItemsPerPage'])
            params = params_utils.update_params({'currentPage': 1, 'maxItemsPerPage': 50}, headers.environ['QUERY_STRING'])
            holders = sorted(self.__holders_repository.get_holders(params), key=lambda holder: holder.holder_id)
            return {
                'currentPage': params['currentPage'],
                'maxItemsPerPage': params['maxItemsPerPage'],
                'holders': [
                    {'holder_id': holder.holder_id, 'name': holder.name, 'document': holder.document} for holder in holders
                ]
            }
        except NotFound:
            raise HolderNotFound('No holders found.')

    def get_holder_by_id(self, holder_id):
        try:
            holder = self.__holders_repository.get_holder_by_id(holder_id)
            return {'holder_id': holder.holder_id, 'name': holder.name, 'document': holder.document}
        except NoResultFound:
            raise HolderNotFound('Holder not found.')

    def create_holder(self, body):
        self.__validator.validate_body(body, post_holder_schema)
        if self.__document_already_exists(body['documentsssss']):
            raise DocumentAlreadyExists('Document already exists.')
        holder = self.__holders_repository.create_holder(self.__holder_builder.holder_builder(body))
        return {
                'message': 'Holder created with success!',
                'holder': {
                    'holder_id': holder.holder_id,
                    'name': holder.name,
                    'document': holder.document
                }
            }

    def __document_already_exists(self, document):
        return True if (self.__holders_repository.get_holder_by_document(document)) else False

    def update_holder(self, holder_id, body):
        self.__validator.validate_body(body, put_holder_schema)
        try:
            existent_holder = self.__holders_repository.get_holder_by_id(holder_id)
            existent_holder.name = body['name']
            self.__holders_repository.update_holder()
            return {
                'message': 'Holder updated with success!',
                'holder': {
                    'holder_id': existent_holder.holder_id,
                    'name': existent_holder.name,
                    'document': existent_holder.document
                }
            }
        except NoResultFound:
            raise HolderNotFound('Holder not found.')
