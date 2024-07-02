from sqlalchemy import Column, BigInteger, String, Numeric, TIMESTAMP
from config.db_config import Base


class TransactionModel(Base):
    __tablename__ = "transactions"
    __table_args__ = {"schema": "accounts"}

    transaction_id = Column(String, primary_key=True)
    transaction_type = Column(String)
    transaction_value = Column(Numeric)
    transaction_date = Column(TIMESTAMP)
    origin_account = Column(BigInteger)
    destination_account = Column(BigInteger)
