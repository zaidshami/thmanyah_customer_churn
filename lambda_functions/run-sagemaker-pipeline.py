import boto3

def lambda_handler(event, context):
    try:
        # Define target pipeline and region
        target_region = 'us-east-1'
        pipeline_name = 'CustomerChurnPipeline'

        # Create SageMaker client in the target region
        sagemaker_client = boto3.client('sagemaker', region_name=target_region)

        # Optionally include parameters here
        response = sagemaker_client.start_pipeline_execution(
            PipelineName=pipeline_name,
            PipelineExecutionDisplayName='TriggeredFromLambda',
            PipelineParameters=[
            {
                "Name": "ProcessingInstanceType",
                "Value": "ml.m5.large"
            },
            {
                "Name": "TrainingInstanceType",
                "Value": "ml.m5.xlarge"
            }
            ]
        )

        return {
            'statusCode': 200,
            'body': f"Pipeline started: {response['PipelineExecutionArn']}"
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': f"Error starting pipeline: {str(e)}"
        }