import boto3
import json
import os
from dotenv import load_dotenv

'''
Purpose of this project is to export our staging prod API, analyze it and make changes if necessary, 
compare it against our dev API, and then import the changed API.
'''
load_dotenv("./.env")

api_id = os.getenv("API_ID")
dev_stage = os.getenv("DEV_STAGE") 
prod_stage = os.getenv("PROD_STAGE")
export_type = "oas30"
dev_region = os.getenv("AWS_REGION_DEV")


dev_session = boto3.Session(region_name=dev_region, aws_access_key_id=os.getenv("ACCESS_KEY"),
                      aws_secret_access_key=os.getenv("SECRET_KEY"))
dev_client = dev_session.client('apigateway')


'''
Exports prod api from AWS and returns as json.
'''
def export_api(api_id, stage_name, export_type):
    response = dev_client.get_export(
        restApiId=api_id,
        stageName=stage_name, 
        exportType=export_type,
        parameters={'extensions': 'integrations'}
    )
    
    export_data = response['body'].read().decode('utf-8')
    return export_data

#print(export_api(api_id, prod_stage, export_type))

'''
Writes exported api to local file.
'''
def write_data():
    current_path = os.getcwd()
    print(f"Current path: {current_path}")

    # Check if we are already in the desired folder
    if current_path == "./apis":
        pass
    else:
        try:
            # Navigate to the desired folder
            os.chdir("./apis")
        except FileNotFoundError:
            print("./apis not found")
    exported_data = export_api(api_id, dev_stage, export_type)
    with open(f'{api_id}_import.json', 'w') as file:
        file.write(exported_data)


'''
Imports API to dev stage.

NOTE: 
securitySchemes
im_localRequest_authorizer
im_jwt_authorizer


In the exported API,these three pieces had an "x-amazon-apigateway-authtype: custom" 
line that had to be removed in order for the API to be imported.
'''
def import_api():
    current_path = os.getcwd()
    if current_path == "./apis":
        pass
    else:
        try:
            # Navigate to the desired folder
            os.chdir("./apis")
        except FileNotFoundError:
            print("./apis not found")
    with open(f'{api_id}_import.json', 'r') as file:
        api_content = file.read()

    response = dev_client.put_rest_api(
        restApiId=api_id,
        mode="overwrite",
        body=api_content
    )

    return response

'''
def create_test_api():
    response = dev_client.create_rest_api(
        name="Dev_Test_API_JS",
        description="Test API for MIS-3131",
        cloneFrom="8q1seu2r5g"
    )

    return response
'''

def dev_vs_prod():
    prod = export_api(api_id, prod_stage, export_type)
    dev = export_api(api_id, dev_stage, export_type)

    prod_json_str = json.dumps(prod, sort_keys=True)
    dev_json_str = json.dumps(dev, sort_keys=True)

    assert prod_json_str == dev_json_str, "The 'prod' and 'dev' JSON objects are not equal."

#dev_vs_prod()
#print("after write, before import")
import_api()