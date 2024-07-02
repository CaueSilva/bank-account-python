from http import HTTPStatus

from jsonschema.exceptions import ValidationError

from exceptions.exceptions import DocumentAlreadyExists, HolderNotFound, AccountNotFound, StatusNotAllowed, \
    InsufficientBalance, AccountAlreadyExistentByHolder, TransactionNotFound
from services.holders_service import HoldersService
from services.accounts_service import AccountsService
from services.transactions_service import TransactionsService
from util.log_config import logger
from flask_restx import Namespace, Resource
from flask import request

api = Namespace('v1', description='Holder and Account operations.')
holders_service = HoldersService()
accounts_service = AccountsService()
transactions_service = TransactionsService()


@api.route("/v1/holder")
class HolderController(Resource):

    @api.doc(responses={
        200: 'Success',
        400: 'Bad request',
        401: 'Authentication error',
        403: 'Authorization error',
        500: 'Internal server error'
    })
    def get(self):
        try:
            logger.info({'message': 'Starting GET all holders request.'})
            headers = request.headers
            result = holders_service.get_all_holders(headers)
            logger.info({'message': 'Found {} holders.'.format(0 if not result['holders'] else str(len(result['holders'])))})
            return result, HTTPStatus.OK
        except ValidationError as e:
            logger.error({'message': 'An error occurred while performing the request.', 'exception': e})
            return {'error': f'{e.args[0]}'}, HTTPStatus.BAD_REQUEST
        except HolderNotFound as e:
            logger.error({'message': 'An error occurred while performing the request.', 'exception': e})
            return {'error': f'{e.args[0]}'}, HTTPStatus.NOT_FOUND
        except Exception as e:
            logger.error({'message': 'An error occurred while performing the request.', 'exception': e})
            return {'error': f'An error occurred while performing the request: {e.args[0]}'}, HTTPStatus.INTERNAL_SERVER_ERROR

    @api.doc(responses={
        200: 'Success',
        400: 'Bad request',
        401: 'Authentication error',
        403: 'Authorization error',
        500: 'Internal server error'
    })
    def post(self):
        try:
            logger.info({'message': 'Starting POST holder request.'})
            body = request.json
            result = holders_service.create_holder(body)
            logger.info({'message': 'Holder created with success. Holder ID: {}'.format(result['holder']['holder_id'])})
            return result, HTTPStatus.CREATED
        except DocumentAlreadyExists as e:
            logger.error({'message': 'An error occurred while performing the request.', 'exception': e})
            return {'error': f'{e.args[0]}'}, HTTPStatus.BAD_REQUEST
        except ValidationError as e:
            logger.error({'message': 'An error occurred while performing the request.', 'exception': e})
            return {'error': f'{e.args[0]}'}, HTTPStatus.BAD_REQUEST
        except Exception as e:
            logger.error({'message': 'An error occurred while performing the request.', 'exception': e})
            return {'error': f'An error occurred while performing the request: {e.args[0]}'}, HTTPStatus.INTERNAL_SERVER_ERROR


@api.route("/v1/holder/<int:holder_id>")
class HolderController(Resource):

    @api.doc(responses={
        200: 'Success',
        400: 'Bad request',
        401: 'Authentication error',
        403: 'Authorization error',
        500: 'Internal server error'
    })
    def get(self, holder_id):
        try:
            logger.info({'message': f'Starting GET holder by ID request.', 'holder_id': holder_id})
            holder = holders_service.get_holder_by_id(holder_id)
            logger.info({'message': 'Found holder by ID.', 'holder_id': holder_id})
            return holder, HTTPStatus.OK
        except HolderNotFound as e:
            logger.error({'message': 'An error occurred while performing the request.', 'holder_id': holder_id, 'exception': e})
            return {'error': f'{e.args[0]}'}, HTTPStatus.NOT_FOUND
        except Exception as e:
            logger.error({'message': 'An error occurred while performing the request.', 'holder_id': holder_id, 'exception': e})
            return {'error': f'An error occurred while performing the request: {e.args[0]}'}, HTTPStatus.INTERNAL_SERVER_ERROR

    @api.doc(responses={
        200: 'Success',
        400: 'Bad request',
        401: 'Authentication error',
        403: 'Authorization error',
        500: 'Internal server error'
    })
    def put(self, holder_id):
        try:
            logger.info({'message': 'Starting PUT holder by ID request.', 'holder_id': holder_id})
            body = request.json
            result = holders_service.update_holder(holder_id, body)
            logger.info({'message': f'Holder update with success.', 'holder_id': holder_id})
            return result, HTTPStatus.OK
        except ValidationError as e:
            logger.error({'message': 'An error occurred while performing the request.', 'holder_id': holder_id, 'exception': e})
            return {'error': f'{e.args[0]}'}, HTTPStatus.BAD_REQUEST
        except HolderNotFound as e:
            logger.error({'message': 'An error occurred while performing the request.', 'holder_id': holder_id, 'exception': e})
            return {'error': f'{e.args[0]}'}, HTTPStatus.NOT_FOUND
        except Exception as e:
            logger.error({'message': 'An error occurred while performing the request.', 'holder_id': holder_id, 'exception': e})
            return {'error': f'An error occurred while performing the request: {e.args[0]}'}, HTTPStatus.INTERNAL_SERVER_ERROR


@api.route("/v1/account")
class AccountController(Resource):

    @api.doc(responses={
        200: 'Success',
        400: 'Bad request',
        401: 'Authentication error',
        403: 'Authorization error',
        500: 'Internal server error'
    })
    def post(self):
        try:
            logger.info({'message': 'Starting POST account request.'})
            body = request.json
            result = accounts_service.create_account(body)
            logger.info({'message': 'Account created with success. Account ID: {}'.format(result['account']['account_id'])})
            return result, HTTPStatus.CREATED
        except HolderNotFound as e:
            logger.error({'message': 'An error occurred while performing the request.', 'exception': e})
            return {'error': f'{e.args[0]}'}, HTTPStatus.NOT_FOUND
        except AccountAlreadyExistentByHolder as e:
            logger.error({'message': 'An error occurred while performing the request.', 'exception': e})
            return {'error': f'{e.args[0]}'}, HTTPStatus.BAD_REQUEST
        except ValidationError as e:
            logger.error({'message': 'An error occurred while performing the request.', 'exception': e})
            return {'error': f'{e.args[0]}'}, HTTPStatus.BAD_REQUEST
        except Exception as e:
            logger.error({'message': 'An error occurred while performing the request.', 'exception': e})
            return {'error': f'An error occurred while performing the request: {e.args[0]}'}, HTTPStatus.INTERNAL_SERVER_ERROR

    @api.doc(responses={
        200: 'Success',
        400: 'Bad request',
        401: 'Authentication error',
        403: 'Authorization error',
        500: 'Internal server error'
    })
    def get(self):
        try:
            logger.info({'message': 'Starting GET all accounts request.'})
            headers = request.headers
            result = accounts_service.get_all_accounts(headers)
            logger.info({'message': 'Found {} accounts.'.format(0 if not result['accounts'] else str(len(result['accounts'])))})
            return result, HTTPStatus.OK
        except ValidationError as e:
            logger.error({'message': 'An error occurred while performing the request.', 'exception': e})
            return {'error': f'{e.args[0]}'}, HTTPStatus.BAD_REQUEST
        except AccountNotFound as e:
            logger.error({'message': 'An error occurred while performing the request.', 'exception': e})
            return {'error': f'{e.args[0]}'}, HTTPStatus.NOT_FOUND
        except Exception as e:
            logger.error({'message': 'An error occurred while performing the request.', 'exception': e})
            return {'error': f'An error occurred while performing the request: {e.args[0]}'}, HTTPStatus.INTERNAL_SERVER_ERROR


@api.route("/v1/account/<int:account_id>")
class AccountController(Resource):
    @api.doc(responses={
        200: 'Success',
        400: 'Bad request',
        401: 'Authentication error',
        403: 'Authorization error',
        500: 'Internal server error'
    })
    def get(self, account_id):
        try:
            logger.info({'message': 'Starting GET all accounts request.', 'account_id': account_id})
            result = accounts_service.get_account_by_id(account_id)
            logger.info({'message': 'Found Account by ID.', 'account_id': account_id})
            return result, HTTPStatus.OK
        except AccountNotFound as e:
            logger.error({'message': 'An error occurred while performing the request.', 'exception': e})
            return {'error': f'{e.args[0]}'}, HTTPStatus.NOT_FOUND
        except Exception as e:
            logger.error({'message': 'An error occurred while performing the request.', 'exception': e})
            return {'error': f'An error occurred while performing the request: {e.args[0]}'}, HTTPStatus.INTERNAL_SERVER_ERROR


@api.route("/v1/account/<int:account_id>/block")
class AccountController(Resource):

    @api.doc(responses={
        200: 'Success',
        400: 'Bad request',
        401: 'Authentication error',
        403: 'Authorization error',
        500: 'Internal server error'
    })
    def post(self, account_id):
        try:
            logger.info({'message': 'Starting POST method to block account.', 'account_id': account_id})
            result = accounts_service.block_account(account_id)
            logger.info({'message': 'Account blocked with success.', 'account_id': account_id})
            return result, HTTPStatus.OK
        except StatusNotAllowed as e:
            logger.error({'message': 'An error occurred while performing the request.', 'exception': e})
            return {'error': f'{e.args[0]}'}, HTTPStatus.BAD_REQUEST
        except AccountNotFound as e:
            logger.error({'message': 'An error occurred while performing the request.', 'exception': e})
            return {'error': f'{e.args[0]}'}, HTTPStatus.NOT_FOUND
        except Exception as e:
            logger.error({'message': 'An error occurred while performing the request.', 'exception': e})
            return {'error': f'An error occurred while performing the request: {e.args[0]}'}, HTTPStatus.INTERNAL_SERVER_ERROR


@api.route("/v1/account/<int:account_id>/reactivate")
class AccountController(Resource):

    @api.doc(responses={
        200: 'Success',
        400: 'Bad request',
        401: 'Authentication error',
        403: 'Authorization error',
        500: 'Internal server error'
    })
    def post(self, account_id):
        try:
            logger.info({'message': 'Starting POST method to reactivate account.', 'account_id': account_id})
            result = accounts_service.reactivate_account(account_id)
            logger.info({'message': 'Account reactivated with success.', 'account_id': account_id})
            return result, HTTPStatus.OK
        except StatusNotAllowed as e:
            logger.error({'message': 'An error occurred while performing the request.', 'exception': e})
            return {'error': f'{e.args[0]}'}, HTTPStatus.BAD_REQUEST
        except AccountNotFound as e:
            logger.error({'message': 'An error occurred while performing the request.', 'exception': e})
            return {'error': f'{e.args[0]}'}, HTTPStatus.NOT_FOUND
        except Exception as e:
            logger.error({'message': 'An error occurred while performing the request.', 'exception': e})
            return {'error': f'An error occurred while performing the request: {e.args[0]}'}, HTTPStatus.INTERNAL_SERVER_ERROR


@api.route("/v1/account/<int:account_id>/close")
class AccountController(Resource):

    @api.doc(responses={
        200: 'Success',
        400: 'Bad request',
        401: 'Authentication error',
        403: 'Authorization error',
        500: 'Internal server error'
    })
    def post(self, account_id):
        try:
            logger.info({'message': 'Starting POST method to close account.', 'account_id': account_id})
            result = accounts_service.close_account(account_id)
            logger.info({'message': 'Account closed with success.', 'account_id': account_id})
            return result, HTTPStatus.OK
        except StatusNotAllowed as e:
            logger.error({'message': 'An error occurred while performing the request.', 'exception': e})
            return {'error': f'{e.args[0]}'}, HTTPStatus.BAD_REQUEST
        except AccountNotFound as e:
            logger.error({'message': 'An error occurred while performing the request.', 'exception': e})
            return {'error': f'{e.args[0]}'}, HTTPStatus.NOT_FOUND
        except Exception as e:
            logger.error({'message': 'An error occurred while performing the request.', 'exception': e})
            return {'error': f'An error occurred while performing the request: {e.args[0]}'}, HTTPStatus.INTERNAL_SERVER_ERROR


@api.route("/v1/transactions")
class TransactionController(Resource):
    @api.doc(responses={
        200: 'Success',
        400: 'Bad request',
        401: 'Authentication error',
        403: 'Authorization error',
        500: 'Internal server error'
    })
    def get(self):
        try:
            logger.info({'message': 'Starting GET all transactions request.'})
            headers = request.headers
            result = transactions_service.get_all_transactions(headers)
            logger.info({'message': 'Found {} transactions.'.format(0 if not result['transactions'] else str(len(result['transactions'])))})
            return result, HTTPStatus.OK
        except ValidationError as e:
            logger.error({'message': 'An error occurred while performing the request.', 'exception': e})
            return {'error': f'{e.args[0]}'}, HTTPStatus.BAD_REQUEST
        except TransactionNotFound as e:
            logger.error({'message': 'An error occurred while performing the request.', 'exception': e})
            return {'error': f'{e.args[0]}'}, HTTPStatus.NOT_FOUND
        except Exception as e:
            logger.error({'message': 'An error occurred while performing the request.', 'exception': e})
            return {'error': f'An error occurred while performing the request: {e.args[0]}'}, HTTPStatus.INTERNAL_SERVER_ERROR


@api.route("/v1/transactions/<string:transaction_id>")
class TransactionController(Resource):
    @api.doc(responses={
        200: 'Success',
        400: 'Bad request',
        401: 'Authentication error',
        403: 'Authorization error',
        500: 'Internal server error'
    })
    def get(self, transaction_id):
        try:
            logger.info({'message': 'Starting GET transaction by ID request.', 'transaction_id': transaction_id})
            result = transactions_service.get_transaction_by_id(transaction_id)
            logger.info({'message': 'Found transaction by ID.', 'transaction_id': transaction_id})
            return result, HTTPStatus.OK
        except TransactionNotFound as e:
            logger.error({'message': 'An error occurred while performing the request.', 'exception': e})
            return {'error': f'{e.args[0]}'}, HTTPStatus.NOT_FOUND
        except Exception as e:
            logger.error({'message': 'An error occurred while performing the request.', 'exception': e})
            return {'error': f'An error occurred while performing the request: {e.args[0]}'}, HTTPStatus.INTERNAL_SERVER_ERROR


@api.route("/v1/transactions/deposit")
class TransactionController(Resource):

    @api.doc(responses={
        200: 'Success',
        400: 'Bad request',
        401: 'Authentication error',
        403: 'Authorization error',
        500: 'Internal server error'
    })
    def post(self):
        try:
            logger.info({'message': 'Starting POST deposit to account.'})
            body = request.json
            result = transactions_service.deposit(body)
            logger.info({'message': 'Deposit made successfully.'})
            return result, HTTPStatus.OK
        except StatusNotAllowed as e:
            logger.error({'message': 'An error occurred while performing the request.', 'exception': e})
            return {'error': f'{e.args[0]}'}, HTTPStatus.BAD_REQUEST
        except ValidationError as e:
            logger.error({'message': 'An error occurred while performing the request.', 'exception': e})
            return {'error': f'{e.args[0]}'}, HTTPStatus.BAD_REQUEST
        except Exception as e:
            logger.error({'message': 'An error occurred while performing the request.', 'exception': e})
            return {'error': f'An error occurred while performing the request: {e.args[0]}'}, HTTPStatus.INTERNAL_SERVER_ERROR


@api.route("/v1/transactions/withdraw")
class TransactionController(Resource):

    @api.doc(responses={
        200: 'Success',
        400: 'Bad request',
        401: 'Authentication error',
        403: 'Authorization error',
        500: 'Internal server error'
    })
    def post(self):
        try:
            logger.info({'message': 'Starting POST withdraw from account.'})
            body = request.json
            result = transactions_service.withdraw(body)
            logger.info({'message': 'Withdraw made successfully.'})
            return result, HTTPStatus.OK
        except InsufficientBalance as e:
            logger.error({'message': 'An error occurred while performing the request.', 'exception': e})
            return {'error': f'{e.args[0]}'}, HTTPStatus.BAD_REQUEST
        except StatusNotAllowed as e:
            logger.error({'message': 'An error occurred while performing the request.', 'exception': e})
            return {'error': f'{e.args[0]}'}, HTTPStatus.BAD_REQUEST
        except ValidationError as e:
            logger.error({'message': 'An error occurred while performing the request.', 'exception': e})
            return {'error': f'{e.args[0]}'}, HTTPStatus.BAD_REQUEST
        except Exception as e:
            logger.error({'message': 'An error occurred while performing the request.', 'exception': e})
            return {'error': f'An error occurred while performing the request: {e.args[0]}'}, HTTPStatus.INTERNAL_SERVER_ERROR


@api.route("/v1/transactions/transfer")
class TransactionController(Resource):

    @api.doc(responses={
        200: 'Success',
        400: 'Bad request',
        401: 'Authentication error',
        403: 'Authorization error',
        500: 'Internal server error'
    })
    def post(self):
        try:
            logger.info({'message': 'Starting POST method to transfer values between accounts.'})
            body = request.json
            result = transactions_service.transfer(body)
            return result, HTTPStatus.OK
        except InsufficientBalance as e:
            logger.error({'message': 'An error occurred while performing the request.', 'exception': e})
            return {'error': f'{e.args[0]}'}, HTTPStatus.BAD_REQUEST
        except StatusNotAllowed as e:
            logger.error({'message': 'An error occurred while performing the request.', 'exception': e})
            return {'error': f'{e.args[0]}'}, HTTPStatus.BAD_REQUEST
        except ValidationError as e:
            logger.error({'message': 'An error occurred while performing the request.', 'exception': e})
            return {'error': f'{e.args[0]}'}, HTTPStatus.BAD_REQUEST
        except Exception as e:
            logger.error({'message': 'An error occurred while performing the request.', 'exception': e})
            return {'error': f'An error occurred while performing the request: {e.args[0]}'}, HTTPStatus.INTERNAL_SERVER_ERROR
