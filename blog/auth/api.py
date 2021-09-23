from fastapi.security.oauth2 import OAuth2PasswordBearer
from blog.auth.models import Token, UserCreate, UserOut
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from .services import AuthService, get_current_user

router = APIRouter(prefix='/auth')


@router.post('/sign-in', response_model=Token)
async def sign_in(
	form_data: OAuth2PasswordRequestForm = Depends(),
	service: AuthService = Depends(),
):
	return await service.login_user(form_data.username, form_data.password)


@router.post('/sign-up', response_model=Token)
async def sign_up(
	user: UserCreate,
	service: AuthService = Depends()
):
	return await service.create_user(user)


@router.get('/user')
async def get_user(username: OAuth2PasswordBearer = Depends(get_current_user)):
	return {"username": username}