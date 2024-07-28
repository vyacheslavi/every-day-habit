up:
	docker compose -f docker-compose-ci.yml up -d
up-local:
	docker compose -f docker-compose-local.yml up -d


down:
	docker compose -f docker-compose-ci.yml down -d
down-local:
	docker compose -f docker-compose-local.yml down -d


build:
	docker compose -f docker-compose-ci.yml up -d --build

rebuild:
	docker-compose -f docker-compose-local.yml up -d --force-recreate --no-deps --build $(container)
