from fastapi import HTTPException, status


class HTTP_401_Exception(HTTPException):

	def __init__(self, detail: str):
		super().__init__(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail=detail,
			headers={
				'WWW-Authenticate': 'Bearer',
			}
		)