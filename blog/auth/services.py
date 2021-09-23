from blog.database.db import get_async_session
import datetime
import sqlalchemy
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.hash import bcrypt

from blog.auth.models import Token
from blog.settings import settings
from blog.database import AsyncSession
from .exceptions import HTTP_401_Exception
from .models import UserCreate, Token
from blog.database import schemas


oauth2_scheme = OAuth2PasswordBearer('/auth/sign-in')

def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
	return AuthService.validate_token(token)



class AuthService:

	@classmethod
	def verify_password(cls, password: str, password_hash: str) -> bool:
		return bcrypt.verify(password, password_hash)

	@classmethod
	def hash_password(cls, password: str) -> str:
		return bcrypt.hash(password)

	@classmethod
	def create_token(username: str) -> Token:
		now = datetime.now()
		token_lifetime = datetime.timedelta(seconds=settings.JWT_TOKEN_LIFETIME)
		payload = {
			'iat': now,
			'nbf': now,
			'exp': now + token_lifetime,
			'sub': username,
		}
		token = jwt.encode(
			payload,
			settings.JWT_SECRET,
			algorithm=settings.JWT_ALGORITHM,
		)

		return Token(access_token=token)

	@classmethod
	def validate_token(cls, token: str) -> str:

		'''
		Extracts username from token
		'''

		exception = HTTP_401_Exception("Could not validate credentials")

		try:
			payload = jwt.decode(
				token,
				settings.JWT_SECRET,
				algorithms=[settings.JWT_ALGORITHM],
			)
		except JWTError:
			raise exception from None

		username = payload.get('sub')

		if not username:
			raise exception from None

		return username

	def __init__(
		self,
		session: AsyncSession = Depends(get_async_session)
	) -> None:

		self.session = session

	async def create_user(self, user_data: UserCreate) -> Token:
		async with self.session.begin():
			user = schemas.User(
				username=user_data.username,
				password_hash=self.hash_password(user_data.password),
				email=user_data.email,
				first_name=user_data.first_name,
				last_name=user_data.last_name
			)

			self.session.add(user)

			await self.session.commit()

		return self.create_token(user_data.username)

	async def login_user(self, username: str, password: str) -> Token:
		exception = HTTP_401_Exception("Username or password are incorrect")

		async with self.session.begin():
			user = await (
				self.session
				.select(schemas.User)
				.query(schemas.User.username == username)
				.first()
				.scalars()
			)

		if not user:
			raise exception

		if not self.verify_password(password, username.password_hash):
			raise exception

		return self.create_token(username)