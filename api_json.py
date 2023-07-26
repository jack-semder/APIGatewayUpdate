import boto3
import json
import os
from dotenv import load_dotenv

load_dotenv("./.env")

api_id = os.getenv("API_ID")
prod_stage = os.getenv("PROD_STAGE") #prod
dev_stage = os.getenv("DEV_STAGE") #dev
export_type = "oas30"
prod_region = os.getenv("AWS_REGION_PROD")
dev_region = os.getenv("AWS_REGION_DEV")


prod_session = boto3.Session(region_name=prod_region, aws_access_key_id=os.getenv("ACCESS_KEY"),
                      aws_secret_access_key=os.getenv("SECRET_KEY"))
prod_client = prod_session.client('apigateway')

dev_session = boto3.Session(region_name=dev_region, aws_access_key_id=os.getenv("ACCESS_KEY"),
                      aws_secret_access_key=os.getenv("SECRET_KEY"))
dev_client = prod_session.client('apigateway')

def export_api(api_id, stage_name, export_type):
    response = prod_client.get_export(
        restApiId=api_id,
        stageName=stage_name, 
        exportType=export_type,
        parameters={'extensions': 'integrations'}
    )
    
    export_data = response['body'].read().decode('utf-8')
    return export_data

print(export_api(api_id, prod_stage, export_type))
'''
def get_lambda_arn(api_id, resource_id):
    try:
        response = prod_client.get_integration(
            restApiId=api_id,
            resourceId=resource_id,
            httpMethod='POST'  
        )

        # Extract and return the Lambda function ARN from the integration response
        #print(response['uri'])
        return response['uri']
    except prod_client.exceptions.NotFoundException:
        print(f"Integration not found for API '{api_id}' and resource '{resource_id}'.")
    except Exception as e:
        print(f"An error occurred: {e}")


print(export_api(api_id, stage_name1, export_type))

def import_api(api_id, stage_name, api_definition):
    #with open(export_api(api_id, stage_name, export_type), 'r') as f:
        #api_definition = f.read()

    client.put_rest_api(
        restApiId=api_id,
        mode='overwrite',
        body=api_definition
    )

    client.create_deployment(
    restApiId=api_id,
    stageName=stage_name
)


def compare():
    prod = export_api()
    dev = import_api()

    if prod == dev:
        pass

def write_data():
    export_data = export_api(api_id, stage_name1, export_type)

    folder_path = "./apis"

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file_path = os.path.join(folder_path, f'{api_id}{stage_name1}.json')

    with open(file_path, 'w') as file:
        file.write(export_data)

    import_api(api_id, stage_name2, export_data)

write_data()
'''
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