from api_json import export_api, import_api
import os

def main():
    # Replace 'your_api_id' with the actual API ID you want to export
    api_id = os.getenv("API_ID")
    stage = os.getenv("PROD_STAGE")
    export_type = "oas30"

    # Export the API
    import_api()
'''
    # Replace 'your_resource_id' with the resource ID associated with the Lambda integration
    resource_id = 'k8rbce'

    # Retrieve the Lambda ARN
    lambda_arn = get_lambda_arn(api_id, resource_id)

    print(f'For this API {api_id}: \n API export: {exported_api} \n Associated Lambda: {lambda_arn}')
'''
if __name__ == "__main__":
    main()
