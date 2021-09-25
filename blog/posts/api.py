from typing import List, Optional

from starlette import status
from blog.auth.services import get_current_user
from fastapi.param_functions import Depends
from blog.auth.models import UserOut
from fastapi import APIRouter
from .models import PostCreate, Post
from .services import PostService, creator_access_only


router = APIRouter(prefix='/posts', tags=['Posts'])


@router.post('/create', response_model=Post)
async def create_post(
	post: PostCreate,
	creator: UserOut = Depends(get_current_user),
	service: PostService = Depends()
) -> Post:

	return await service.create_post(post, creator)


@router.get('/get', response_model=List[Post], response_model_exclude_none=True)
async def get_post(
	creator: Optional[str] = None,
	post_id: Optional[int] = None,
	return_content: bool = False,
	service: PostService = Depends()
) -> List[Post]:
	return await service.get_post(
		service.query_to_filters_list(creator, post_id),
		return_content=return_content
	)

@router.delete('/delete', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
	post: Post = Depends(creator_access_only),
	service: PostService = Depends()
):
	await service.delete_post(post.id)