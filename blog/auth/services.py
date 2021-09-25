from blog.database.db import get_async_session
import datetime
import sqlalchemy
from sqlalchemy.exc import IntegrityError
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.hash import bcrypt

from blog.auth.models import Token
from blog.settings import settings
from blog.database import AsyncSession
from .exceptions import HTTP_401_Exception, HTTP_422_Exception
from .models import UserCreate, Token, UserOut
from blog.database import schemas


oauth2_scheme = OAuth2PasswordBearer('/auth/sign-in')

async def get_current_user(
	token: str = Depends(oauth2_scheme),
	session: AsyncSession = Depends(get_async_session)
) -> UserOut:

	username = AuthService.validate_token(token)

	async with session.begin():

		query = (
			sqlalchemy
			.select(schemas.User)
			.where(schemas.User.username == username)
		)
		user = (await session.execute(query)).first()

		if user:
			user = user[0]
		else:
			raise HTTP_401_Exception("Current user does not exist")

		return UserOut.from_orm(user)



class AuthService:

	@classmethod
	def verify_password(cls, password: str, password_hash: str) -> bool:
		return bcrypt.verify(password, password_hash)

	@classmethod
	def hash_password(cls, password: str) -> str:
		return bcrypt.hash(password)

	@classmethod
	def create_token(cls, username: str) -> Token:
		now = datetime.datetime.utcnow()
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
		except JWTError as e:
			raise HTTP_401_Exception(str(e)) from None

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

			try:

				await self.session.commit()

			except IntegrityError as error:

				raise HTTP_422_Exception("Username is alredy exists")


		return self.create_token(user_data.username)

	async def login_user(self, username: str, password: str) -> Token:
		exception = HTTP_401_Exception("Username or password are incorrect")

		async with self.session.begin():
			query = (
				sqlalchemy
				.select(schemas.User)
				.where(schemas.User.username == username)
			)
			user = (await self.session.execute(query)).first()

		if user:
			user = user[0]
		else:
			raise exception

		if not self.verify_password(password, user.password_hash):
			raise exception

		return self.create_token(username)