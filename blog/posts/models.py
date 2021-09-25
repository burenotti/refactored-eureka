from typing import Optional
from pydantic.fields import Field
from blog.database.db import Base
from pydantic import BaseModel
from ..auth.models import User, UserOut


class BasePost(BaseModel):

	title: str = Field(min_length=3, max_length=100)


class PostWithContent(BasePost):

	content: Optional[str] = Field(max_length=5000)


class PostCreate(PostWithContent):
	pass


class Post(PostWithContent):
	id: int
	creator: UserOut

	class Config:
		orm_mode = True