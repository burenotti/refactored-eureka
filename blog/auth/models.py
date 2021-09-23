from pydantic import BaseModel, Field, EmailStr


class BaseUser(BaseModel):
    username: str = Field(max_length=32)


class UserOut(BaseUser):
    first_name: str = Field(max_length=64)
    last_name: str = Field(max_length=64)
    email: EmailStr = Field()


class UserCreate(UserOut):
    password: str


class User(UserOut):
    password_hash: str


class Token(BaseModel):
	access_token: str
	token_type: str = 'bearer'