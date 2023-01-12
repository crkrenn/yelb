#!/usr/bin/env python3

import yaml
import sys

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

def add_tags(dictionary, tags):
    key_name = "Tags"
    print(f"Adding the following '{key_name}' to the cloud compose definition: {tags}")
    results = dict_extract(key_name, dictionary)
    for result in results:
        for key, value in tags.items():
            result[key_name].append({'Key': key, 'Value': value})

def update_keys(dictionary, new_keys):
    print(f"Making the following updates to the cloud compose definition: {new_keys}")
    for key, value in new_keys.items():
        results = dict_extract(key, dictionary)
        for result in results:
            result[key] = value

if len(sys.argv) < 7:
    print("Missing arguments.")
    print("This script requires <old_filename> <new_filename> <billing_tag> <service_url>.")
old_filename = sys.argv[1]
new_filename = sys.argv[2]
billing_tag = sys.argv[3]
service_url = sys.argv[4]
service_name = sys.argv[5]
aws_region = sys.argv[6]


with open(old_filename, "r") as stream:
    try:
        dictionary = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)
        sys.exit()

# print("before add tags")
# results = dict_extract("Tags", dictionary)
# for result in results:
#     print(result)

new_tags = {"billing_tag": billing_tag}
add_tags(dictionary, new_tags)

replacement_values = {"ClusterName": service_name, "LogGroupName": f"/docker-compose/{service_name}"}
update_keys(dictionary, replacement_values)

with open(new_filename, 'w') as outfile:
    yaml.dump(dictionary, outfile, default_flow_style=False)



