#!/usr/bin/env python3

import yaml
import sys
import os
# from common import ssl_certificate_arn, stack_description, logical_to_physical_id

def dict_extract(key, var):
    if hasattr(var,'items'): # hasattr(var,'items') for python 3
        for k, v in var.items(): # var.items() for python 3
            if k == key:
                yield var
            if isinstance(v, dict):
                for result in dict_extract(key, v):
                    yield result
            elif isinstance(v, list):
                for d in v:
                    for result in dict_extract(key, d):
                        yield result

def add_elements_to_item(item_key, dictionary, tags):
    print(f"Adding the following '{item_key}' to the cloud compose definition: {tags}")
    results = dict_extract(item_key, dictionary)
    for result in results:
        for key, value in tags.items():
            if type(result[item_key]) == list:
                result[item_key].append({'Key': key, 'Value': value})
            elif type(result[item_key]) == dict:
                result[item_key][key] = value
            else:
                raise ValueError("type must be list or dict")

def update_keys(dictionary, new_keys):
    print(f"Making the following updates to the cloud compose definition: {new_keys}")
    for key, value in new_keys.items():
        results = dict_extract(key, dictionary)
        for result in results:
            result[key] = value

try:
    old_filename = os.environ["RAW_COMPOSE_FILE"]
    new_filename = os.environ["EDITED_COMPOSE_FILE"]
    billing_tag = os.environ["BILLING_TAG"]
    service_name = os.environ["SERVICE_NAME"]
    aws_region = os.environ["AWS_REGION"]
    aws_hosted_zone = os.environ["AWS_HOSTED_ZONE"]
except KeyError as err:
    print("ERROR: missing environment variable!")
    print(err)
    sys.exit()

# certificate_arn = ssl_certificate_arn(service_name, aws_hosted_zone)
# my_description = stack_description(stack_name)
# listener_arn = logical_to_physical_id(my_description, "Listener")[0]

with open(old_filename, "r") as stream:
    try:
        dictionary = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)
        sys.exit()

new_elements = {"billing_tag": billing_tag}
add_elements_to_item("Tags", dictionary, new_elements)

# new_elements = {"LoadBalancerCertificate": {
#   "Properties" : {
#       "Certificates" : [ certificate_arn ],
#       "ListenerArn" : listener_arn
#     },
#   "Type" : "AWS::ElasticLoadBalancingV2::ListenerCertificate",
# }}
# add_elements_to_item("Resources", dictionary, new_elements)

replacement_values = {"ClusterName": service_name, "LogGroupName": f"/docker-compose/{service_name}"}
update_keys(dictionary, replacement_values)

with open(new_filename, 'w') as outfile:
    yaml.dump(dictionary, outfile, default_flow_style=False)



