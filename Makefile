up:
	docker compose -f docker-compose-ci.yml up -d
build:
	docker compose -f docker-compose-ci.yml up -d --build
upwatch:
	docker compose -f docker-compose-ci.yml up -d --watch
rebuild:
	docker compose -f docker-compose-ci.yml up -d --no-deps --build <container>

# Recreate single container
# docker-compose -f docker-compose-local.yml up -d --force-recreate --no-deps --build app
