from fastapi import HTTPException, status
from pydantic import ValidationError


class HTTP_401_Exception(HTTPException):

	def __init__(self, detail: str):
		super().__init__(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail=detail,
			headers={
				'WWW-Authenticate': 'Bearer',
			}
		)


class HTTP_422_Exception(HTTPException):

	def __init__(self, detail: str):
		super().__init__(
			status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
			detail=detail,

		)
