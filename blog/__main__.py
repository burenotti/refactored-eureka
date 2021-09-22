import uvicorn
import sys
from .settings import settings

def main(_):

	uvicorn.run(
		'blog.app:app',
		host=settings.HOST,
		port=settings.PORT,
		reload=settings.UVICORN_RELOAD,
		workers=settings.UVICORN_WORKERS,
	)


if __name__ == '__main__':
	main(sys.argv)
