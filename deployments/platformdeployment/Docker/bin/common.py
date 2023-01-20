import boto3
import pydig

def ssl_certificate_arn(service_name, aws_hosted_zone):
    client_acm = boto3.client('acm')
    response = client_acm.request_certificate(
        DomainName=f'{service_name}.{aws_hosted_zone}',
        ValidationMethod='DNS',
    )
    return response['CertificateArn']

def stack_description(stack_name):
    client_cf = boto3.client('cloudformation')
    response = client_cf.list_stack_resources(
        StackName=stack_name,
    )
    return response

def logical_to_physical_id(description="", suffix=""):
    if not description or not suffix:
        print(
            "ERROR: function requires both a description and a logical "
            "id suffix")
    summary_list = description["StackResourceSummaries"]
    results = []
    len_suffix = len(suffix)
    for resource in summary_list:
        if resource["LogicalResourceId"][-len_suffix:] == suffix:
            results.append(resource["PhysicalResourceId"])
    return results

def validate_caa(hosted_zone, dns_service):
    result = pydig.query(hosted_zone,'CAA')
    success = False
    for item in result:
        if dns_service in item:
            success = True
    return success
