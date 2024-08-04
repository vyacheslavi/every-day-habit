THIS_FILE := $(lastword $(MAKEFILE_LIST))
.PHONY: help build up start down destroy stop restart logs logs-api ps login-timescale login-api db-shell
help:
	make -pRrq  -f $(THIS_FILE) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'


down-local:
	docker compose -f docker-compose-local.yml down
up-local:
	docker compose -f docker-compose-local.yml up -d


up:
	docker compose -f docker-compose-ci.yml up -d
down:
	docker compose -f docker-compose-ci.yml down
build:
	docker compose -f docker-compose-ci.yml up -d --build
rebuild:
	docker compose -f docker-compose-ci.yml up -d --force-recreate --no-deps --build $(s)
logs:
	docker-compose -f docker-compose-ci.yml logs --tail=100 -f $(s)
logs-app:
	docker-compose -f docker-compose-ci.yml logs --tail=100 -f app
ps:
	docker-compose -f docker-compose-ci.yml ps
