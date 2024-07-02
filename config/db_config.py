from sqlalchemy import create_engine, NullPool
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy

url_db = 'postgresql://postgres:admin@localhost:5432/bank-account'

Base = declarative_base()
db = SQLAlchemy()
Base.query = db.session.query_property()

engine = create_engine(url_db, poolclass=NullPool)
Session = sessionmaker(bind=engine)
session = Session()
