from sqlalchemy import Column, BigInteger, String
from config.db_config import Base


class HolderModel(Base):
    __tablename__ = "holders"
    __table_args__ = {"schema": "holders"}

    holder_id = Column(BigInteger, primary_key=True)
    name = Column(String)
    document = Column(String)
