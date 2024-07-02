from unittest import TestCase
from unittest.mock import patch

from jsonschema.exceptions import ValidationError
from sqlalchemy.exc import NoResultFound
from werkzeug.datastructures.headers import EnvironHeaders
from werkzeug.exceptions import NotFound

from exceptions.exceptions import DocumentAlreadyExists, HolderNotFound
from tests.builder import return_holder_creation_body, return_holder_update_body, return_list_of_holders, return_holder
from services.holders_service import HoldersService
from builders.holder_builder import HolderBuilder


class HoldersServiceTest(TestCase):
    holders_service = HoldersService()
    holder_builder = HolderBuilder()
    default_current_page = 1
    default_max_items_per_page = 50

    @patch('repository.holders_repository.HoldersRepository.create_holder')
    @patch('repository.holders_repository.HoldersRepository.get_holder_by_document')
    def test_holder_was_created_with_success(self,
                                             get_holder_by_document_mock,
                                             create_holder_mock):
        body = return_holder_creation_body()
        get_holder_by_document_mock.return_value = False
        create_holder_mock.return_value = self.holder_builder.holder_builder(body)

        result = self.holders_service.create_holder(body)

        self.assertTrue(result['holder'])
        self.assertEqual('Holder created with success!', result['message'])

    def test_holder_creation_returned_document_validation_error(self):
        body = return_holder_creation_body()
        short_document = '1234567891'
        body['document'] = short_document

        with self.assertRaises(ValidationError) as exception_result:
            self.holders_service.create_holder(body)

        self.assertEqual(f"'{short_document}' is too short", exception_result.exception.args[0])

        long_document = '123456789178'
        body['document'] = long_document

        with self.assertRaises(ValidationError) as exception_result:
            self.holders_service.create_holder(body)

        self.assertEqual(f"'{long_document}' is too long", exception_result.exception.args[0])

    @patch('repository.holders_repository.HoldersRepository.get_holder_by_document')
    def test_holder_creation_returned_error_by_document_already_existing_on_database(self,
                                                                                     get_holder_by_document_mock):
        get_holder_by_document_mock.return_value = True

        with self.assertRaises(DocumentAlreadyExists) as exception_result:
            self.holders_service.create_holder(return_holder_creation_body())

        self.assertEqual('Document already exists.', exception_result.exception.args[0])

    @patch('repository.holders_repository.HoldersRepository.update_holder')
    @patch('repository.holders_repository.HoldersRepository.get_holder_by_id')
    def test_holder_update_made_successfully(self,
                                             get_holder_by_id_mock,
                                             update_holder_mock):
        holder = return_holder()
        get_holder_by_id_mock.return_value = holder
        body_update = return_holder_update_body()

        result = self.holders_service.update_holder(0, body_update)

        self.assertEqual('Holder updated with success!', result['message'])
        self.assertEqual(holder.holder_id, result['holder']['holder_id'])
        self.assertEqual(holder.document, result['holder']['document'])
        self.assertEqual(body_update['name'], result['holder']['name'])

    @patch('repository.holders_repository.HoldersRepository.get_holder_by_id')
    def test_holder_update_returned_error_when_holder_is_not_found(self,
                                                                   get_holder_by_id_mock):
        get_holder_by_id_mock.side_effect = NoResultFound()

        with self.assertRaises(HolderNotFound) as exception_result:
            self.holders_service.update_holder(0, return_holder_update_body())

        self.assertEqual('Holder not found.', exception_result.exception.args[0])

    @patch('repository.holders_repository.HoldersRepository.get_holders')
    def test_get_all_holders_returned_result_successfully_without_pagination_params(self,
                                                                                    get_holders_mock):
        get_holders_mock.return_value = return_list_of_holders()
        headers = EnvironHeaders({"QUERY_STRING": ''})
        result = self.holders_service.get_all_holders(headers)

        self.assertEqual(self.default_current_page, result['currentPage'])
        self.assertEqual(self.default_max_items_per_page, result['maxItemsPerPage'])
        self.assertEqual(2, len(result['holders']))

    @patch('repository.holders_repository.HoldersRepository.get_holders')
    def test_exception_is_raised_when_no_holder_is_found(self,
                                                         get_holders_mock):
        get_holders_mock.side_effect = NotFound()
        headers = EnvironHeaders({"QUERY_STRING": ''})

        with self.assertRaises(HolderNotFound) as exception_result:
            self.holders_service.get_all_holders(headers)

        self.assertEqual('No holders found.', exception_result.exception.args[0])

    @patch('repository.holders_repository.HoldersRepository.get_holder_by_id')
    def test_get_holder_by_id_return_success(self,
                                             get_holder_by_id_mock):
        get_holder_by_id_mock.return_value = return_holder()

        result = self.holders_service.get_holder_by_id(1)

        self.assertTrue(result)

    @patch('repository.holders_repository.HoldersRepository.get_holder_by_id')
    def test_get_holder_by_id_raises_exception(self,
                                               get_holder_by_id_mock):
        get_holder_by_id_mock.side_effect = NoResultFound()

        with self.assertRaises(HolderNotFound) as exception_result:
            self.holders_service.get_holder_by_id(1)

        self.assertEqual('Holder not found.', exception_result.exception.args[0])
