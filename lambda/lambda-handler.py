import json
import urllib.parse
import boto3

print('Loading function')

s3 = boto3.client('s3')


def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(
        event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    try:
        print("Downloading file from s3")
        s3.download_file(bucket, key, '/tmp/' + key)
        print("File downloaded")
        with open('/tmp/' + key, 'r') as file:
            contents = file.read()
            print(f"File contents: {contents}")

    except Exception as e:
        print(e)
        print(
            f"Error getting object: {key} from bucket: {bucket}. Make sure they exist and your bucket permissions are correct.")
