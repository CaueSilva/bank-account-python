# Bank Account Python

## 🎯 Project's Goal

This project allows the user to manage Holders and Accounts, such as create, update and list information. Also, is possible to create transactions to an Account, such as Deposits, Withdraws and Transfers between Accounts.

## 🔧 Stack

This project was developed using [Python 3.9](https://www.python.org/downloads/release/python-390/) as main and only programming language, [Postgres 13.15](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads) as database system and [PgAdmin4 7.8](https://www.postgresql.org/ftp/pgadmin/pgadmin4/v7.8/windows/) as database management system.

## 💻 Endpoints

1. [Holders](#holders)
   1. [Create Holder](#create-holder)
   2. [Update Holder](#update-holder)
   3. [Get Holder By ID](#get-holder-by-id)
   4. [List All Holders](#list-all-holders)
2. [Accounts](#accounts)
   1. [Create Account](#create-account)
   2. [Block Account](#block-account)
   3. [Reactivate Account](#reactivate-account)
   4. [Close Account](#close-account)
   5. [Get Account by ID](#get-account-by-id)
   6. [List All Accounts](#list-all-accounts)
3. [Transactions](#transactions)
   1. [Deposit to an Account](#deposit-to-an-account)
   2. [Withdraw from an Account](#withdraw-from-an-account)
   3. [Transfer values between Accounts](#transfer-values-between-accounts)
   4. [Get Transaction by ID](#get-transaction-by-id)
   5. [List All Transactions](#list-all-transactions)

## 👥Holders

Endpoints to create, update and list Holders.

### Create Holder

This endpoint allows the user to register a Holder. If the request is succesfull, the API will return the Holder ID.

Path: `/v1/holder`

HTTP Method: `POST`

Body fields:

`name`: Holder's name (String), min. of 3 characters;

`document`: Holder's document (String), min. of 11 characters, max of 14.

#### Request Body:

```json
{
  "name": "John",
  "document": "12345678910"
}
```

#### Responses by Http Codes:

```json
{
  "201": {
    "message": "Holder created with success!",
    "holder": {
        "holder_id": 0,
        "name": "John",
        "document": "12345678910"
    }
  },
  "400": [
    {
      "error": "Document already exists."
    },
    {
      "error": "'{document}' is too long"
    },
    {
      "error": "'{document}' is too short"
    }
  ],
  "500": {
    "error": "An error occurred while performing the request: {error}"
  }
}
```
### Update Holder

This endpoint allows the user to update a Holder's name, as it's ID and Document are unique. If the request is succesfull, the API will return the Holder's updated information.

Path: `/v1/holder/{holder_id}`

HTTP Method: `PUT`

Path Variable:

`holder_id`: Holder's ID.

Body fields:

`name`: Holder's new name (String), min of 3 characters;

#### Request Body:

```json
{
  "name": "John Cena"
}
```

#### Responses by Http Codes:

```json
{
  "200": {
    "message": "Holder updated with success!",
    "holder": {
        "holder_id": 9,
        "name": "John Cena",
        "document": "12345678919"
    }
  },
  "400": [
    {
       "error": "'{name}' is too short"
    }, 
    {
      "error": "{name} is not of type 'string'"    
    }, 
    {
      "error": "{document} is not of type 'string'"    
    }
  ],
  "500": {
    "error": "An error occurred while performing the request: {error}"
  }
}
```

### Get Holder By ID

This endpoint allows the user to list a single holder by its ID.

Path: `/v1/holder/{holder_id}`

HTTP Method: `GET`

Path Variable: 

`holder_id`: Holder's ID.

#### Responses by Http Codes:

```json
{
  "200": {
    "holder_id": 9,
    "name": "John Cena",
    "document": "12345678919"
  },
  "404": {
      "error": "Holder not found."
  },
  "500": {
    "error": "An error occurred while performing the request: {error}"
  }
}
```

### List All Holders

This endpoint allows the user to list all Holders in Database. 

Path: `/v1/holder`

HTTP Method: `GET`

Query parameters:

`currentPage`: Request's current page (integer);

`maxItemsPerPage`: Count of items returned by page (integer).

#### Responses by Http Codes:

```json
{
  "200": {
    "currentPage": 1,
    "maxItemsPerPage": 50,
    "holders": [
        {
            "holder_id": 1,
            "name": "Holder One",
            "document": "12345678910"
        },
        {
            "holder_id": 2,
            "name": "Holder Two",
            "document": "01987654321"
        }
    ]
  }, 
  "400": {
     "error": "Filter not allowed."
  },
  "404": {
      "error": "No holders found."
  },
  "500": {
    "error": "An error occurred while performing the request: {error}"
  }
}
```

## 💰Accounts

Endpoints to create, update Accounts status and list accounts.

### Create Account

This endpoint allows the user to register an Account to a Holder. If request is successful, the API will return the Account Information.

Path: `/v1/account`

HTTP Method: `POST`

Body fields:

`holder_id`: Holder's ID (integer), minimum 1.

#### Request Body:

```json
{
    "holder_id": 1
}
```

#### Responses by Http Codes:

```json
{
  "201": {
    "message": "Account created with success!",
    "account": {
        "account_id": 1,
        "holder_id": 1,
        "balance": "0.00",
        "status": "ACTIVE"
    }
  }, 
  "400": [
     {
        "error": "Holder already have an Account."
     },
     {
        "error": "{holder_id} is less than the minimum of 1"  
     },
     {
        "error": "'{holder_id}' is not of type 'number'"  
     }
  ],
  "404": {
      "error": "Holder not found."
  },
  "500": {
    "error": "An error occurred while performing the request: {error}"
  }
}
```

### Block Account

This endpoint allows the user to block an Account.

Path: `/v1/account/{account_id}/block`

HTTP Method: `POST`

Path Variable: 

`account_id`: Account ID.

#### Responses by Http Codes:

```json
{
  "200": {
    "message": "Account blocked.",
    "account": {
        "account_id": 1,
        "holder_id": 1,
        "balance": "0.00",
        "status": "BLOCKED"
    }
  }, 
  "400": {
    "error": "Account is already closed."
  },
  "404": {
    "error": "Account not found."
  },
  "500": {
    "error": "An error occurred while performing the request: {error}"
  }
}
```

### Reactivate Account

This endpoint allows the user to reactivate an Account.

Path: `/v1/account/{account_id}/reactivate`

HTTP Method: `POST`

Path Variable: 

`account_id`: Account ID.

#### Responses by Http Codes:

```json
{
  "200": {
    "message": "Account reactivated.",
    "account": {
        "account_id": 1,
        "holder_id": 1,
        "balance": "0.00",
        "status": "ACTIVE"
    }
  }, 
  "400": {
    "error": "Account is already closed."
  },
  "404": {
    "error": "Account not found."
  },
  "500": {
    "error": "An error occurred while performing the request: {error}"
  }
}
```

### Close Account

This endpoint allows the user to close an Account.

Path: `/v1/account/{account_id}/close`

HTTP Method: `POST`

Path Variable: 

`account_id`: Account ID.

#### Responses by Http Codes:

```json
{
  "200": {
    "message": "Account closed.",
    "account": {
        "account_id": 9,
        "holder_id": 8,
        "balance": "0.00",
        "status": "CLOSED"
    }
  }, 
  "400": {
    "error": "Account is already closed."
  },
  "404": {
    "error": "Account not found."
  },
  "500": {
    "error": "An error occurred while performing the request: {error}"
  }
}
```

### Get Account By ID

This endpoint allows the user to list a single Account by its ID.

Path: `/v1/account/{account_id}`

HTTP Method: `GET`

Path Variable: 

`account_id`: Account ID.

#### Responses by Http Codes:

```json
{
  "200": {
    "account_id": 1,
    "holder_id": 1,
    "balance": "0.00",
    "status": "ACTIVE"
  },
  "404": {
      "error": "Account not found."
  },
  "500": {
    "error": "An error occurred while performing the request: {error}"
  }
}
```

### List All Accounts

This endpoint allows the user to list all Accounts in Database. 

Path: `/v1/account`

HTTP Method: `GET`

Query parameters:

`currentPage`: Request's current page (integer);

`maxItemsPerPage`: Count of items returned by page (integer).

#### Responses by Http Codes:

```json
{
  "200": {
    "currentPage": 1,
    "maxItemsPerPage": 50,
    "accounts": [
        {
            "account_id": 1,
            "holder_id": 1,
            "balance": "0",
            "status": "CLOSED"
        },
        {
            "account_id": 2,
            "holder_id": 2,
            "balance": "1009.99",
            "status": "ACTIVE"
        }
	]
  }, 
  "400": {
     "error": "Filter not allowed."
  },
  "404": {
      "error": "No accounts found."
  },
  "500": {
    "error": "An error occurred while performing the request: {error}"
  }
}
```

## 💸Transactions

Endpoints to create Deposits, Withdraws, Transfers or list Transactions information.

### Deposit to an Account

This endpoint allows the user to deposit values to an Account.

Path: `/v1/transactions/deposit`

HTTP Method: `POST`

Body fields:

`account_id`: Account ID (integer) that will receive the deposit, minimum 1;
`value`: Value (Numeric) to be deposited to the Account ID, minimum 0.01.

#### Request Body:

```json
{
    "account_id": 1,
    "value": 200.50
}
```

#### Responses by Http Codes:

```json
{
  "201": {
    "message": "Deposit made successfully!",
    "transaction": {
        "transaction_id": "b87c0e3a-d0d9-4076-be00-0058f3be4579",
        "transaction_type": "DEPOSIT",
        "transaction_value": "200.50",
        "transaction_date": "2024-07-02T19:39:57",
        "account_id": 1
    }
  }, 
  "400": [
     {
        "error": "Account is not active."
     },
     {
        "error": "{account_id} is less than the minimum of 1" 
     },
     {
        "error": "'{account_id}' is not of type 'number'" 
     },
     {
        "error": "'{value}' is not of type 'number'" 
     },
     {
        "error": "{value} is less than the minimum of 0.01" 
     }
  ],
  "404": {
      "error": "Holder not found."
  },
  "500": {
    "error": "An error occurred while performing the request: {error}"
  }
}
```

### Withdraw from an Account

This endpoint allows the user to withdraw values from an Account.

Path: `/v1/transactions/withdraw`

HTTP Method: `POST`

Body fields:

`account_id`: Account ID (integer) that will have the amount withdrawn from the actual balance, minimum 1;
`value`: Value (Numeric) to be withdrawn from the Account ID, minimum 0.01.

#### Request Body:

```json
{
    "account_id": 1,
    "value": 10.00
}
```

#### Responses by Http Codes:

```json
{
  "201": {
    "message": "Withdraw made successfully!",
    "transaction": {
        "transaction_id": "a2ddfc8f-43cc-430c-8d89-9cc43ef3f370",
        "transaction_type": "WITHDRAW",
        "transaction_value": "10.00",
        "transaction_date": "2024-07-02T19:42:33",
        "account_id": 1
    }
  }, 
  "400": [
     {
        "error": "Account is not active."
     },
     {
        "error": "Account doesn't have enough balance to complete operation."
     },
     {
        "error": "{account_id} is less than the minimum of 1" 
     },
     {
        "error": "{value} is less than the minimum of 0.01" 
     },
     {
        "error": "'{account_id}' is not of type 'number'" 
     },
     {
        "error": "'{value}' is not of type 'number'" 
     }
  ],
  "404": {
      "error": "Holder not found."
  },
  "500": {
    "error": "An error occurred while performing the request: {error}"
  }
}
```

### Transfer Values Between Accounts

This endpoint allows to transfer values from an Account to other Account.

Path: `/v1/transactions/transfer`

HTTP Method: `POST`

Body fields:

`original_account_id`: Account ID (integer) that will have the amount debited from the actual balance, minimum 1;
`destination_account_id`: Account ID (integer) that will receive the amount debited from the original Account, minimum 1;
`value`: Value (Numeric) to be transferred between the Accounts, minimum 0.01.

#### Request Body:

```json
{
  "original_account_id": 1,
  "destination_account_id": 2,
  "value": 10
}
```

#### Responses by Http Codes:

```json
{
  "201": {
    "message": "Transfer completed with success.",
    "transaction": {
        "transaction_id": "634bfa34-2579-43a9-8529-6a476e148fd3",
        "transaction_type": "TRANSFER",
        "transaction_value": "10.00",
        "transaction_date": "2024-07-02T19:56:27",
        "origin_account": 1,
        "destination_account": 2
    }
  }, 
  "400": [
     {
        "error": "Origin Account is not active."
     },
     {
        "error": "Destination Account is not active."
     },
     {
        "error": "Origin Account doesn't have enough balance to complete operation."
     },
     {
        "error": "{account_id} is less than the minimum of 1" 
     },
     {
        "error": "{value} is less than the minimum of 0.01" 
     },
     {
        "error": "'{original_account_id}' is not of type 'number'" 
     },
     {
        "error": "'{destination_account_id}' is not of type 'number'" 
     },
     {
        "error": "'{value}' is not of type 'number'" 
     }
  ],
  "404": {
      "error": "Holder not found."
  },
  "500": {
    "error": "An error occurred while performing the request: {error}"
  }
}
```

### Get Transaction by ID

This endpoint allows the user to list a single Transaction by its ID.

Path: `/v1/transactions/{transaction_id}`

HTTP Method: `GET`

Path Variable: 

`transaction_id`: Transaction ID.

#### Responses by Http Codes:

```json
{
  "200": {
    "transaction_id": "2a35fb8f-362e-4748-aaa1-67348e0fc94b",
    "transaction_type": "WITHDRAW",
    "transaction_value": "5.00",
    "transaction_date": "2024-06-24T12:20:46",
    "origin_account": 1,
    "destination_account": ""
  },
  "404": {
      "error": "Transaction not found."
  },
  "500": {
    "error": "An error occurred while performing the request: {error}"
  }
}
```
### List All Transactions

This endpoint allows the user to list all Transactions in Database. 

Path: `/v1/transactions`

HTTP Method: `GET`

Query parameters:

`currentPage`: Request's current page (integer);

`maxItemsPerPage`: Count of items returned by page (integer).

#### Responses by Http Codes:

```json
{
  "200": {
    "currentPage": 1,
    "maxItemsPerPage": 50,
    "transactions": [
        {
            "transaction_id": "2a35fb8f-362e-4748-aaa1-67348e0fc94b",
            "transaction_type": "WITHDRAW",
            "transaction_value": "5.00",
            "transaction_date": "2024-06-24T12:20:46",
            "origin_account": 1,
            "destination_account": ""
        },
        {
            "transaction_id": "a909e604-ef0a-404e-a3d1-72958668265d",
            "transaction_type": "WITHDRAW",
            "transaction_value": "5.00",
            "transaction_date": "2024-06-24T12:24:39",
            "origin_account": 1,
            "destination_account": ""
        }
	]
  }, 
  "400": {
     "error": "Filter not allowed."
  },
  "404": {
      "error": "No transactions found."
  },
  "500": {
    "error": "An error occurred while performing the request: {error}"
  }
}
```
