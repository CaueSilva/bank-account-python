from sqlalchemy import Column, BigInteger, Integer, Numeric
from config.db_config import Base


class AccountModel(Base):
    __tablename__ = "accounts"
    __table_args__ = {"schema": "accounts"}

    account_id = Column(BigInteger, primary_key=True)
    holder_id = Column(BigInteger)
    balance = Column(Numeric)
    status = Column(Integer)
