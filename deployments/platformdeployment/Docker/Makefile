#!/usr/bin/env make
include .env
export $(shell sed 's/=.*//' .env)

BILLING_TAG ?= yelb_dev
SERVICE_URL ?= yelb.example.com
SERVICE_NAME ?= yelb
AWS_REGION ?= us-west-2

AWS_HOSTED_ZONE_ID ?= XXXXXXXXXXXXX
AWS_ROOT_DOMAIN ?= example.com

RAW_COMPOSE_FILE = cloud_compose.yaml
EDITED_COMPOSE_FILE = cloud_compose_new.yaml

import_dns:
	-@echo "attempting to authenticate with aws dns"; \
	cd terraform; \
	terraform init; \
	export TFVAR_aws_root_domain=${AWS_ROOT_DOMAIN}; \
	terraform import aws_route53_zone.root ${AWS_HOSTED_ZONE_ID}

test: import_dns
	echo foo

convert: ## convert docker file to cloud compose file
	docker context use myecscontext2
	docker compose convert > ${RAW_COMPOSE_FILE}

cloud-compose: convert ## update cloud compose file with custom features
	bin/update_cloud_compose.py ${RAW_COMPOSE_FILE} ${EDITED_COMPOSE_FILE} \
		${BILLING_TAG} ${SERVICE_URL} ${SERVICE_NAME} ${AWS_REGION}

create-stack: cloud-compose ## launch updated cloud compose file
	aws cloudformation create-stack \
		--stack-name ${SERVICE_NAME}-stack \
		--template-body file://${EDITED_COMPOSE_FILE} \
		--region ${AWS_REGION} \
		--capabilities CAPABILITY_IAM

describe-stack: ## describe stack
	aws cloudformation list-stack-resources \
		--stack-name ${SERVICE_NAME}-stack \

stack-url: ## get URL of stack load balancer
	@aws cloudformation describe-stack-resource \
		--stack-name ${SERVICE_NAME}-stack \
		--logical-resource-id LoadBalancer | \
		jq '.StackResourceDetail.PhysicalResourceId' | \
		xargs aws elbv2 describe-load-balancers --load-balancer-arns | \
		jq '"http://" + (.LoadBalancers | .[0] | .DNSName)'

delete-stack:  ## delete running stack
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