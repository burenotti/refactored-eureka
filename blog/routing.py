from fastapi import APIRouter


global_router = APIRouter()


from blog import (
	auth,
	posts
)

global_router.include_router(auth.router)
global_router.include_router(posts.router)