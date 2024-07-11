up:
	docker compose -f docker-compose-local.yml up -d
build:
	docker compose -f docker-compose-local.yml up -d --build
upwatch:
	docker compose -f docker-compose-local.yml up -d --watch

down:
	docker compose -f docker-compose-local.yml down -d  --remove-orphans

remove-w:
	docker rm -vf $(docker ps -aq)

# Recreate single container
# docker-compose -f docker-compose-local.yml up -d --force-recreate --no-deps --build app
