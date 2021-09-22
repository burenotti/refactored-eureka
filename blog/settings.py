from pydantic import BaseSettings


class Settings(BaseSettings):

	# Uvicorn

	HOST: str = "localhost"
	PORT: int = 5000
	UVICORN_RELOAD: bool = 1
	UVICORN_WORKERS: int = 1

	# Database

	DB_URL: str

	# JWT

	JWT_ALGORITHM = "HS_256"
	JWT_SECRET: str
	JWT_TOKEN_LIFETIME: int = 3600 # One hour
