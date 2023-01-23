BASE_ENV ?= .env
PROD_ENV ?= prod.env
DEV_ENV ?= dev.env
DOCKER_ENV ?= docker_temp.env

export ENV_FILE = /dev/null

# all:
# 	@echo "make PROD"
# 	@echo "make DEV"

# TTD: make PROD; make DEV
include ${BASE_ENV}
export $(shell sed 's/=.*//' ${BASE_ENV})

PROD: ## Run in prod mode (e.g. `make PROD start`, etc.)
	@echo Running in prod mode
	$(eval ENV_FILE = prod.env)
	$(eval include ${ENV_FILE})
	$(eval export $(shell sed 's/=.*//' ${ENV_FILE}))

DEV: ## Run in dev mode (e.g. `make DEV start`, etc.)
	@echo Running in dev mode
	$(eval ENV_FILE = dev.env)
	$(eval include ${ENV_FILE})
	$(eval export $(shell sed 's/=.*//' ${ENV_FILE}))

DETACHED: ## Run docker in "detached" mode.
	$(eval export DOCKER_DETACHED=--detach)

docker_env:
	$(shell cat ${BASE_ENV} > ${DOCKER_ENV})
	$(shell cat ${ENV_FILE} >> ${DOCKER_ENV})

echo_vars:
	@echo ENV_FILE=${ENV_FILE}

start: docker_env echo_vars ## Start all Docker containers
	@echo Starting
	-docker-compose --env-file ${DOCKER_ENV} up ${DOCKER_DETACHED}

start-rebuild: echo_vars ## Start all Docker containers, [re]building as needed
	docker-compose --env-file ${ENV_FILE} up ${DOCKER_DETACHED}  --build

stop: echo_vars ## Stop all Docker containers
	-docker-compose --env-file ${DOCKER_ENV} down

rm-containers: echo_vars ## Remove Docker containers where (name contains "${SERVICE_NAME}")
	@echo 'removing filtered containers (name contains "${SERVICE_NAME}")'
	@-docker rm -f $(shell docker ps -aq --filter "name=${SERVICE_NAME}")

rm-volumes: echo_vars ## Remove Docker volumes where (name contains "${SERVICE_NAME}")
	@echo 'removing filtered volumes (name contains "${SERVICE_NAME}")'
	@-docker volume rm -f $(shell docker volume ls -q --filter "label=polis_tag=${TAG}")

rm-images: echo_vars ## Remove Docker images where (name contains "${SERVICE_NAME}")
	@echo 'removing filtered images (name contains "${SERVICE_NAME}")'
	@-docker rmi -f $(shell docker images -q --filter "name=${SERVICE_NAME}")

rm-ALL: rm-containers rm-volumes rm-images ## Remove Docker containers, volumes, and images where (name contains "${SERVICE_NAME}")
	@echo Done.

rm-ALL-ALL-TAGS: ## Remove EVERY Docker container, volume, and image on this machine
	-docker rm -f $(shell docker ps -aq)
	-docker rmi -f $(shell docker images -q)
	-docker volume rm $(shell docker volume ls -q)

modify-code:
	cp testing/modified_code/app.component.html \
		../../yelb-ui/clarity-seed-newfiles/src/app

revert-code:
	cp testing/original_code/app.component.html \
		../../yelb-ui/clarity-seed-newfiles/src/app

test: docker_env # test that env variables are set correctly for make and docker
	@echo Running tests
	cat ${DOCKER_ENV}
	@echo env_tag: ${ENV_TAG}

# ifneq ("$(wildcard $(PROD_ENV))","")
#   $(shell cat ${PROD_ENV} >> ${DOCKER_ENV})
#   include ${PROD_ENV}
#   export $(shell sed 's/=.*//' ${PROD_ENV})
# endif

# run from dockerhub
# run from local
# build local

# variables:
# DOCKER_REPO
# TAGS

# pull: echo_vars ## Pull most recent Docker container builds (nightlies)
# 	docker-compose ${COMPOSE_FILE_ARGS} --env-file ${ENV_FILE} pull

# start: echo_vars ## Start all Docker containers
# 	docker-compose ${COMPOSE_FILE_ARGS} --env-file ${ENV_FILE} up ${DOCKER_DETACHED}

# stop: echo_vars ## Stop all Docker containers
# 	-docker-compose ${COMPOSE_FILE_ARGS} --env-file ${ENV_FILE} down


# rm-ALL-ALL-TAGS: ## Remove EVERY Docker container, volume, and image on this machine
# 	-docker rm -f $(shell docker ps -aq)
# 	-docker rmi -f $(shell docker images -q)
# 	-docker volume rm $(shell docker volume ls -q)

# hash: ## Show current short hash
# 	@echo Git hash: ${GIT_HASH}

# start-rebuild: echo_vars ## Start all Docker containers, [re]building as needed
# 	docker-compose ${COMPOSE_FILE_ARGS} --env-file ${ENV_FILE} up ${DOCKER_DETACHED}  --build

# start-FULL-REBUILD: echo_vars stop rm-ALL ## Remove and restart all Docker containers, volumes, and images where (polis_tag="${TAG}")
# 	docker-compose ${COMPOSE_FILE_ARGS} --env-file ${ENV_FILE} build --no-cache
# 	docker-compose ${COMPOSE_FILE_ARGS} --env-file ${ENV_FILE} down
# 	docker-compose ${COMPOSE_FILE_ARGS} --env-file ${ENV_FILE} up ${DOCKER_DETACHED}  --build
# 	docker-compose ${COMPOSE_FILE_ARGS} --env-file ${ENV_FILE} down
# 	docker-compose ${COMPOSE_FILE_ARGS} --env-file ${ENV_FILE} up ${DOCKER_DETACHED}  --build

help:
	@echo 'Usage: make <command>'
	@echo
	@echo 'where <command> is one of the following:'
	@echo
	@grep -E '^[a-z0-9A-Z_-]+:.*?## .*$$' Makefile | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
	@echo
	@echo 'SERVICE_NAME: ${SERVICE_NAME}'
	@echo 'Note: some targets (e.g. ATTACHED) require GNU Make version 3.82 or above.'
.DEFAULT_GOAL := help
