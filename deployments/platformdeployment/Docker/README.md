These configurations had been lightly tested against Docker for Mac and Docker (configured as a single node Swarm cluster).

These two scripts should work against a simple docker host (which includes support for `Swarm legacy` clusters) as well as a `Swarm mode` cluster.

This is a WIP.

TTD:

plan:
* use makefile/terraform to import dns
* use terraform to make vpc and load balancer
* use python and docker-compose to build rest of stack

https://docs.docker.com/cloud/ecs-integration/
Learn cloud formation
Add tags for billing (check source code).
Add custom domain.
add makefile

move makefile variables to prod.env

add variables to shell/terraform

add load balancer to terraform
remove load balancer from cloud formation
add load balancer arn to cloud formation

https://stackoverflow.com/questions/68952765/unable-to-attach-acm-public-certificate-with-alb-listener-using-lambda-across-ac

need to use python with some waiting to apply certificate properly. 

TTD:
add url cert to makefile:
(venv_docker_aws) (base) crkrenn@admins-MacBook-Pro-2 Docker % aws acm  request-certificate \
--domain-name        
[--validation-method <value>]

add load balancer certificate to update_cloud_compose


