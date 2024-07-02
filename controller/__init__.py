from .api_controller import api as account_namespace
from flask_restx import Api

api = Api(
    title='Account API',
    version='1.0.0',
    description='API to create, deposit and withdraw a bank account.'
)

api.add_namespace(account_namespace, path="/")
