from enum import Enum


class TransactionsTypes(Enum):
    WITHDRAW = "WITHDRAW"
    DEPOSIT = "DEPOSIT"
    TRANSFER = "TRANSFER"
