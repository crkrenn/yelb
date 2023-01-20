#!/usr/bin/env make

# TTD: add update stack
# TTD: add certificate, etc.
# add make for route53

# https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-certificatemanager-certificate.html
# https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listenercertificate.html
#https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listener.html

include .env
export $(shell sed 's/=.*//' .env)

BILLING_TAG ?= yelb_dev
SERVICE_NAME ?= yelb

AWS_REGION ?= us-west-2
AWS_HOSTED_ZONE ?= example.com
AWS_HOSTED_ZONE_ID ?= XXXXXXXXXXXXX
# S3_BUCKET ?= XXXXXXXXXXXXX

RAW_COMPOSE_FILE = cloud_compose.yaml
EDITED_COMPOSE_FILE = cloud_compose_new.yaml
TEMP_JSON_FILE = temp.json

export DEBUG=false

DEBUG: ## Run tools in DEBUG, with more diagnostic outputs
	$(eval DEBUG=true)

# load_balancer:
# 	-@echo "attempting to create aws load balancer"; \
# 	cd terraform; \
# 	terraform init; \
#   export TF_VAR_DEBUG=${DEBUG}; \
# 	export TF_VAR_service_name=${SERVICE_NAME}; \
# 	export TF_VAR_hosted_zone=${AWS_HOSTED_ZONE}; \
# 	export TF_VAR_s3_bucket=${S3_BUCKET}; \
# 	export TF_VAR_billing_tag=${BILLING_TAG}; \
# 	terraform plan

dns_input:
	@jq --null-input \
	--arg user "${AWS_REGION}" \
	--arg password "${AWS_HOSTED_ZONE}" \
	'{ \
		"Comment": "CREATE/DELETE/UPSERT a record ", \
		"Changes": [{ \
		"Action": "CREATE", \
					"ResourceRecordSet": { \
								"Name": "a.example.com", \
								"Type": "A", \
								"TTL": 300, \
							"ResourceRecords": [{ "Value": "4.4.4.4"}] \
		}}] \
	}' > ${TEMP_JSON_FILE}; \
	cat ${TEMP_JSON_FILE}
# $ aws route53 change-resource-record-sets --hosted-zone-id ZXXXXXXXXXX --change-batch file://sample.json

# -import_dns:
# -       -@echo "attempting to authenticate with aws dns"; \
# -       cd terraform; \
# -       terraform init; \
#   export TF_VAR_DEBUG=${DEBUG}; \
# -       export TFVAR_aws_root_domain=${AWS_ROOT_DOMAIN}; \
# -       terraform import aws_route53_zone.root ${AWS_HOSTED_ZONE_ID}


convert: ## convert docker file to cloud compose file
	docker context use myecscontext2
	docker compose convert > ${RAW_COMPOSE_FILE}

cloud-compose: convert ## update cloud compose file with custom features
	export DEBUG=${DEBUG}; \
	export RAW_COMPOSE_FILE=${RAW_COMPOSE_FILE}; \
	export EDITED_COMPOSE_FILE=${EDITED_COMPOSE_FILE}; \
	export BILLING_TAG=${BILLING_TAG}; \
	export SERVICE_NAME=${SERVICE_NAME}; \
	export AWS_REGION=${AWS_REGION}; \
	export AWS_HOSTED_ZONE=${AWS_HOSTED_ZONE}; \
	# export SSL_CERTIFICATE=`aws acm request-certificate \
	# 	--domain-name ${SERVICE_NAME}. \
	# 	--validation-method DNS | \
	# 	jq -r ".CertificateArn"` ; \
	bin/update_cloud_compose.py

create-stack: cloud-compose ## launch updated cloud compose file
	aws cloudformation create-stack \
		--stack-name ${SERVICE_NAME}-stack \
		--template-body file://${EDITED_COMPOSE_FILE} \
		--region ${AWS_REGION} \
		--capabilities CAPABILITY_IAM

add-ssl-cert:  ## update-stack add ssl certificate to load balancer
	@export DEBUG=${DEBUG}; \
	export SERVICE_NAME=${SERVICE_NAME}; \
	export AWS_REGION=${AWS_REGION}; \
	export AWS_HOSTED_ZONE=${AWS_HOSTED_ZONE}; \
	export STACK_NAME=${SERVICE_NAME}-stack; \
	bin/add_ssl_certificate.py

noop:
#   export TF_VAR_DEBUG=${DEBUG}; \
	export LOAD_BALANCER_ARN=`aws cloudformation list-stack-resources \
		--stack-name ${SERVICE_NAME}-stack`; \
	aws elbv2 add-listener-certificates \
	--listener-arn arn:aws:elasticloadbalancing:us-west-2:123456789012:listener/app/my-load-balancer/50dc6c495c0c9188/f2f7dc8efc522ab2 --certificates CertificateArn=arn:aws:acm:us-west-2:123456789012:certificate/5cc54884-f4a3-4072-80be-05b9ba72f705
	aws acm request-certificate  \
			@aws cloudformation list-stack-resources \
		--stack-name ${SERVICE_NAME}-stack \
	echo $$SSL_CERTIFICATE_ARN; \


update-stack: cloud-compose ## update stack with current cloud compose file
	@aws cloudformation update-stack \
		--stack-name ${SERVICE_NAME}-stack \
		--template-body file://${EDITED_COMPOSE_FILE} \
		--region ${AWS_REGION} \
		--capabilities CAPABILITY_IAM

describe-stack: ## describe stack
	@aws cloudformation list-stack-resources \
		--stack-name ${SERVICE_NAME}-stack \

stack-status: ## summary of stack status
	@aws cloudformation list-stack-resources \
		--stack-name ${SERVICE_NAME}-stack | \
		grep -e LogicalResourceId -e ResourceStatus

stack-url: ## get URL of stack load balancer
	@aws cloudformation describe-stack-resource \
		--stack-name ${SERVICE_NAME}-stack \
		--logical-resource-id LoadBalancer | \
		jq '.StackResourceDetail.PhysicalResourceId' | \
		xargs aws elbv2 describe-load-balancers --load-balancer-arns | \
		jq -r '"http://" + (.LoadBalancers | .[0] | .DNSName)'

detect-stack-drift: cloud-compose ## detect stack drift
	aws cloudformation detect-stack-drift \
		--stack-name ${SERVICE_NAME}-stack

delete-stack:  ## delete running stack
	aws cloudformation delete-stack --stack-name ${SERVICE_NAME}-stack

help:
	@echo 'Usage: make <command>'
	@echo
	@echo 'where <command> is one of the following:'
	@echo
	@grep -E '^[a-z0-9A-Z_-]+:.*?## .*$$' Makefile | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
	@echo
	@echo 'Note: some targets (e.g. ATTACHED) require GNU Make version 3.82 or above.'
.DEFAULT_GOAL := help
