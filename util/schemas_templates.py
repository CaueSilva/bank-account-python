post_holder_schema = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "minLength": 3
        },
        "document": {
            "type": "string",
            "minLength": 11,
            "maxLength": 11
        }
    },
    "required": [
        "name",
        "document"
    ]
}

put_holder_schema = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "minLength": 3
        }
    },
    "required": [
        "name"
    ]
}

post_account_schema = {
    "type": "object",
    "properties": {
        "holder_id": {
            "type": "number",
            "minimum": 1
        }
    },
    "required": [
        "holder_id"
    ]
}

account_financial_operation_schema = {
    "type": "object",
    "properties": {
        "account_id": {
            "type": "number",
            "minimum": 1
        },
        "value": {
            "type": "number",
            "minimum": 0.01
        }
    },
    "required": [
        "value"
    ]
}

transfer_schema = {
    "type": "object",
    "properties": {
        "original_account_id": {
            "type": "number",
            "minimum": 1
        },
        "destination_account_id": {
            "type": "number",
            "minimum": 1
        },
        "value": {
            "type": "number",
            "minimum": 0.01
        }
    },
    "required": [
        "original_account_id",
        "destination_account_id",
        "value"
    ]
}
