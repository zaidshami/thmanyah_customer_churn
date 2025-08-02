import boto3
import time

def lambda_handler(event, context):
    print('🔁 Starting SageMaker deployment...')

    model_name = event["model_name"]
    endpoint_name = event["endpoint_name"]
    endpoint_config_name = f"{endpoint_name}-config"

    sm_client = boto3.client("sagemaker")

    # Step 1: Delete endpoint if it exists
    try:
        sm_client.describe_endpoint(EndpointName=endpoint_name)
        print(f"🛑 Endpoint {endpoint_name} exists. Deleting...")
        sm_client.delete_endpoint(EndpointName=endpoint_name)

        # Wait until endpoint is deleted (optional but safer)
        while True:
            try:
                sm_client.describe_endpoint(EndpointName=endpoint_name)
                print("⌛ Waiting for endpoint to be deleted...")
                time.sleep(5)
            except sm_client.exceptions.ClientError:
                print("✅ Endpoint deleted.")
                break

    except sm_client.exceptions.ClientError:
        print(f"ℹ️ Endpoint {endpoint_name} does not exist. Skipping delete.")

    # Step 2: Delete endpoint config if exists
    try:
        sm_client.describe_endpoint_config(EndpointConfigName=endpoint_config_name)
        print(f"🛑 Endpoint config {endpoint_config_name} exists. Deleting...")
        sm_client.delete_endpoint_config(EndpointConfigName=endpoint_config_name)
    except sm_client.exceptions.ClientError:
        print(f"ℹ️ Endpoint config {endpoint_config_name} does not exist. Skipping delete.")

    # Step 3: Create new endpoint config
    try:
        print(f"🛠️ Creating new endpoint config: {endpoint_config_name}")
        sm_client.create_endpoint_config(
            EndpointConfigName=endpoint_config_name,
            ProductionVariants=[
                {
                    "VariantName": "AllTraffic",
                    "ModelName": model_name,
                    "InitialInstanceCount": 1,
                    "InstanceType": "ml.t2.medium",
                    "InitialVariantWeight": 1
                }
            ]
        )
    except sm_client.exceptions.ClientError as e:
        return {"status": "error", "message": f"Failed to create endpoint config: {str(e)}"}

    # Step 4: Create endpoint
    try:
        print(f"🚀 Creating new endpoint: {endpoint_name}")
        sm_client.create_endpoint(
            EndpointName=endpoint_name,
            EndpointConfigName=endpoint_config_name
        )
        return {
            "status": "success",
            "endpoint": endpoint_name,
            "endpoint_config": endpoint_config_name
        }

    except sm_client.exceptions.ClientError as e:
        return {"status": "error", "message": f"Failed to create endpoint: {str(e)}"}