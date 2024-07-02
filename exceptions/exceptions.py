

class DocumentAlreadyExists(Exception):

    def __init__(self, message, status_code=400):
        super().__init__(message)
        self.status_code = status_code


class HolderNotFound(Exception):

    def __init__(self, message, status_code=404):
        super().__init__(message)
        self.status_code = status_code


class AccountNotFound(Exception):

    def __init__(self, message, status_code=404):
        super().__init__(message)
        self.status_code = status_code


class InsufficientBalance(Exception):

    def __init__(self, message, status_code=404):
        super().__init__(message)
        self.status_code = status_code


class StatusNotAllowed(Exception):

    def __init__(self, message, status_code=400):
        super().__init__(message)
        self.status_code = status_code


class AccountAlreadyExistentByHolder(Exception):

    def __init__(self, message, status_code=400):
        super().__init__(message)
        self.status_code = status_code


class TransactionNotFound(Exception):

    def __init__(self, message, status_code=404):
        super().__init__(message)
        self.status_code = status_code
