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
