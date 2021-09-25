from fastapi import HTTPException, status
from sqlalchemy.sql.expression import exists
from blog.auth.exceptions import HTTP_401_Exception
import sqlalchemy
from sqlalchemy.orm import defer, selectinload
from typing import List

from fastapi import Depends

from ..database import (
	AsyncSession,
	get_async_session,
	schemas
)
from ..auth.models import UserOut
from ..auth.services import get_current_user

from . import models


async def creator_access_only(
	post_id: int,
	user: UserOut = Depends(get_current_user),
	session: AsyncSession = Depends(get_async_session)
) -> UserOut:
	cursor = await session.execute(
		sqlalchemy
		.select(schemas.Post)
		.options(selectinload(schemas.Post.creator))
		.where(
			(schemas.Post.creator_username == user.username) & \
			(schemas.Post.id == post_id)
		)
	)
	result = cursor.scalar()
	if result:

		return result

	else:

		raise HTTPException(
			detail=(
				"Article does not exists "
				"or you are not allowed to delete it"
			),
			status_code=status.HTTP_404_NOT_FOUND,
		)


class PostService:


	class Filters:

		@classmethod
		def post_id(cls, post_id: int):
			return (schemas.Post.id == post_id)

		@classmethod
		def post_creator(cls, username: str):
			return (schemas.Post.creator_username == username)


	@classmethod
	def query_to_filters_list(
		cls,
		post_creator: str = None,
		post_id: int = None,
	):
		filters = []

		if post_creator:
			filters.append(cls.Filters.post_creator(post_creator))

		if post_id:
			filters.append(cls.Filters.post_id(post_id))

		return filters


	@classmethod
	def join_filters(cls, filters: list):
		if not filters:
			return False

		query = filters[0]

		for filter in filters[1:]:
			query = query & filter

		return query


	def __init__(
		self,
		session: AsyncSession = Depends(get_async_session)
	):

		self.session = session

	async def create_post(
		self,
		post: models.PostCreate,
		creator: UserOut,
	) -> models.Post:

		async with self.session.begin():
			post = schemas.Post(
				title=post.title,
				content=post.content,
				creator_username=creator.username,
			)

			self.session.add(post)

			await self.session.commit()

		return models.Post(
			creator=creator,
			id=post.id,
			title=post.title,
			content=post.content,
		)

	async def get_post(
		self,
		filters: list,
		return_content: bool = True
	) -> List[models.Post]:

		posts = []

		filter = self.join_filters(filters)
		query = (
			sqlalchemy
			.select(schemas.Post)
			.options(selectinload(schemas.Post.creator))
			.where(filter)
		)
		if not return_content:
			query = query.options(defer('content'))

		result = await self.session.execute(query)

		for post in result.fetchall():
			post = post[0]
			posts.append(
				models.Post(
					title=post.title,
					id=post.id,
					creator=post.creator,
					content=(None if not return_content else post.content),
				)
			)

		return posts

	async def delete_post(self, post_id: int):
		await self.session.execute(
			sqlalchemy
			.delete(schemas.Post)
			.where(schemas.Post.id == post_id)
		)
		await self.session.commit()
