from builders.holder_builder import HolderBuilder
from builders.account_builder import AccountBuilder
from builders.transaction_builder import TransactionBuilder
from util.enums.account_status import Status
from util.enums.transactions_types import TransactionsTypes


def return_holder_creation_body():
    return {
        "name": "test",
        "document": "12345678910"
    }


def return_holder_update_body():
    return {
        "name": "test_update"
    }


def return_list_of_holders():
    holders_list = []

    first_holder = HolderBuilder.holder_builder({
            "name": "first name",
            "document": "11111111111"
        })
    first_holder.holder_id = 1

    holders_list.append(first_holder)

    second_holder = HolderBuilder.holder_builder({
        "name": "second name",
        "document": "22222222222"
    })
    second_holder.holder_id = 2

    holders_list.append(second_holder)

    return holders_list


def return_holder():
    holder = HolderBuilder.holder_builder(return_holder_creation_body())
    holder.holder_id = 1
    return holder


def return_account_creation_body():
    return {
        "holder_id": 1
    }


def return_active_account():
    account = AccountBuilder.account_builder(1)
    account.account_id = 1
    return account


def return_blocked_account():
    account = AccountBuilder.account_builder(1)
    account.account_id = 1
    account.status = Status.BLOCKED.value
    return account


def return_closed_account():
    account = AccountBuilder.account_builder(1)
    account.account_id = 1
    account.status = Status.CLOSED.value
    return account


def return_list_of_accounts():
    account_list = []

    account = AccountBuilder.account_builder(1)
    account.account_id = 1
    account_list.append(account)

    account = AccountBuilder.account_builder(2)
    account.account_id = 2
    account_list.append(account)
    return account_list


def return_financial_operation_body():
    return {
        "account_id": 1,
        "value": 1.00
    }


def return_financial_operation(transaction_type):
    body = {
        "value": 100
    }
    return TransactionBuilder.transaction_builder(body, transaction_type, 1)


def return_transfer_body():
    return {
        "original_account_id": 1,
        "destination_account_id": 2,
        "value": 100.00
    }


def return_transfer_operation(body=None):
    if body:
        return TransactionBuilder.transaction_builder(body, TransactionsTypes.TRANSFER.value)
    return TransactionBuilder.transaction_builder(return_transfer_body(), TransactionsTypes.TRANSFER.value)


def return_list_of_transactions():
    transactions_list = []

    transaction = return_transfer_operation()
    transactions_list.append(transaction)

    second_transaction_body = return_transfer_body()
    second_transaction_body['original_account_id'] = 3
    second_transaction_body['destination_account_id'] = 4
    second_transaction_body['value'] = 200

    transaction = return_transfer_operation(second_transaction_body)
    transactions_list.append(transaction)

    return transactions_list

