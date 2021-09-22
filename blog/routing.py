from fastapi import APIRouter


global_router = APIRouter()


from blog import (
	auth,
)

global_router.include_router(auth.router)