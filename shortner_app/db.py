import os
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import async_sessionmaker

sqlite_url = os.getenv("sqlite_url","sqlite+aiosqlite:///urls.db")

connect_args = {"check_same_thread": False}
engine = create_async_engine(sqlite_url, connect_args=connect_args)

sessionlocal = async_sessionmaker(bind=engine,autocommit=False, autoflush=False)

Base = declarative_base()  

async def get_db():

    async with sessionlocal() as db:

        try:
            yield db

        except DBAPIError:

            await db.rollback()
            raise

        finally:

            db.close()