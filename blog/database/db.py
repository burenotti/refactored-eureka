from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from blog.settings import settings


Base = declarative_base()

async_engine = create_async_engine(
	settings.DB_URL,
	echo=True,
)
