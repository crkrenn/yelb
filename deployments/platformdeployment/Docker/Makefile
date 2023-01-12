BILLING_TAG ?= yelb_dev
SERVICE_URL ?= yelb.democracygps.org
SERVICE_NAME ?= yelb
AWS_REGION ?= us-west-2

RAW_COMPOSE_FILE = cloud_compose.yaml
EDITED_COMPOSE_FILE = cloud_compose_new.yaml

convert: ## convert docker file to cloud compose file
	docker context use myecscontext
	docker compose convert > ${RAW_COMPOSE_FILE}

cloud_compose: convert ## update cloud compose file with custom features
	bin/update_cloud_compose.py ${RAW_COMPOSE_FILE} ${EDITED_COMPOSE_FILE} \
		${BILLING_TAG} ${SERVICE_URL} ${SERVICE_NAME} ${AWS_REGION}

create_stack: cloud_compose ## launch updated cloud compose file
    aws cloudformation create-stack \
    	--stack-name ${SERVICE_NAME}-stack \
    	--template-body file://${EDITED_COMPOSE_FILE} \
		--region ${AWS_REGION}

delete_stack:  ## delete running stack
	aws cloudformation delete-stack --stack-name ${SERVICE_NAME}-stack

help:
	@echo 'Usage: make <command>'
	@echo
	@echo 'where <command> is one of the following:'
	@echo
	@grep -E '^[a-z0-9A-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
	@echo
	@echo 'Note: some targets (e.g. ATTACHED) require GNU Make version 3.82 or above.'
.DEFAULT_GOAL := help