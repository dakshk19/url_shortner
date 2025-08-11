import os
from sqlalchemy import create_engine
from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

sqlite_url = os.getenv("sqlite_url","sqlite:///urls.db")

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

sessionlocal = sessionmaker(bind=engine,autocommit=False, autoflush=False)

Base = declarative_base()  

def get_db():

    db = sessionlocal()

    try:
        yield db

    except DBAPIError:

        db.rollback()
        raise

    finally:

        db.close()