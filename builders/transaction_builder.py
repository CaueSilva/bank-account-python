from models.TransactionModel import TransactionModel
import uuid
from datetime import datetime


class TransactionBuilder:

    @staticmethod
    def transaction_builder(body, transaction_type, account_id=None):
        return TransactionModel(
            transaction_id=str(uuid.uuid4()),
            transaction_type=transaction_type,
            transaction_value=body['value'],
            transaction_date=datetime.now(),
            origin_account=account_id if account_id else body['original_account_id'],
            destination_account=None if account_id else body['destination_account_id']
        )
