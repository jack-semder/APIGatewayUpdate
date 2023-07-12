import boto3
import json
import os
from dotenv import load_dotenv


load_dotenv("C:/Users/Jack Semder/PycharmProjects/APIGatewayUpdate/.env")

session = boto3.Session(region_name=os.getenv("AWS_REGION"), aws_access_key_id=os.getenv("ACCESS_KEY"),
                      aws_secret_access_key=os.getenv("SECRET_KEY"))
client = session.client('apigateway')


def export_api_stage(api_id, stage_name, export_type):
    response = client.get_export(
        restApiId=api_id,
        stageName=stage_name, 
        exportType=export_type
    )
    
    export_data = response['body'].read().decode('utf-8')
    return export_data

api_id = os.getenv("API_ID")
stage_name = os.getenv("STAGE_ID")
export_type = "oas30"

export_data = export_api_stage(api_id, stage_name, export_type)

with open(f"{api_id}{stage_name}.json", "w") as f:
    f.write(export_data)



'''
access_key = os.getenv("ACCESS_KEY")
secret_access_key = os.getenv("SECRET_KEY")
region = os.getenv("AWS_REGION")

# Create connection
client = boto3.client('apigateway', region_name=region, aws_access_key_id=access_key,
                      aws_secret_access_key=secret_access_key)

api_id = os.getenv("API_ID")
resource_id = os.getenv("RESOURCE_ID")
apis = client.get_rest_apis()


def api_info(): # get methods
    for api in apis["items"]:
        api_id = api["id"]
        api_name = api["name"]

        print(f"API: {api_name} ({api_id})")

        resources = client.get_resources(restApiId=api_id)
        #print(resources)

        for resource in resources["items"]:
            resource_id = resource["id"]
            resource_path = resource["path"]

            print(f" Resource: {resource_path} ({resource_id})")

def extract_lambda():
    response = client.get_resources(restApiId=api_id)


    # Iterate over the resources to find the Lambda integration
    for item in response['items']:
        resource = item['id']


        # Get the resource methods
        resource_methods = client.get_resource(
            restApiId=api_id,
            resourceId=resource
        )

        #print(resource_methods['items'])


        for http_method, method_details in resource_methods.items():
            print("http_method: ", http_method)
            print("method_details: ", method_details)
            
            integration_id = method_details.get('methodIntegration', {}).get('integrationId')
            print("integration id: ", integration_id)

            if integration_id:
                # Get the integration details
                integration = client.get_integration(
                    restApiId=api_id,
                    resourceId=resource,
                    httpMethod=http_method,
                    integrationId=integration_id
                )
                print("integration: ", integration)

                # Check if the integration type is "AWS_PROXY"
                if integration['type'] == 'LAMBDA_PROXY':
                    lambda_function_arn = integration['uri']
                    print("arn: ", lambda_function_arn)

        if 'lambda_function_arn' in locals():
            # Lambda function ARN found, break the outer loop
            break
'''