docker run --rm \
	--name selectel-pgdocker \
	-e POSTGRES_PASSWORD=password \
	-e POSTGRES_USER=user \
	-e POSTGRES_DB=blog \
	-d -p 5432:5432 -v $HOME/docker/volumes/postgres:/var/lib/postgresql/data postgres
