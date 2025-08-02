import json
import boto3


def lambda_handler(event, context):
    sns = boto3.client('sns')
    topic_arn = 'arn:aws:sns:us-east-1:767397763254:notify-pipeline'

    message = f"🚨 Model failed condition check! Details:\n{json.dumps(event)}"

    sns.publish(
        TopicArn=topic_arn,
        Subject='SageMaker Model Alert',
        Message=message
    )

    return {
        'statusCode': 200,
        'body': 'Notification sent'
    }
