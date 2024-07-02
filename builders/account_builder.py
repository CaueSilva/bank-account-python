from _decimal import Decimal
from util.enums.account_status import Status
from models.AccountModel import AccountModel


class AccountBuilder:

    @staticmethod
    def account_builder(holder_id):
        return AccountModel(holder_id=holder_id, balance=Decimal('0.00'), status=Status.ACTIVE.value)
