up:
	docker compose -f docker-compose-local.yml up -d

down:
	docker compose -f docker-compose-local.yml down --remove-orphans

remove-w:
	docker rm -vf $(docker ps -aq)
