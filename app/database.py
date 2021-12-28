from os import environ

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


db_name = environ.get('DB_NAME')
db_password = environ.get('DB_PASSWORD')
db_server = environ.get('DB_SERVER')
db_user = environ.get('DB_USER')
SQLALCHEMY_DATABASE_URL =\
    f"postgresql+psycopg2://{db_user}:{db_password}@{db_server}/{db_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
