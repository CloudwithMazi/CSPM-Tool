import boto3
import json

def fetch_data(bucket_name: str, object_key: str) -> dict:
    """Fetches data from an S3 bucket and returns it as a dictionary."""
    s3 = boto3.client('s3')
    response = s3.get_object(Bucket=bucket_name, Key=object_key)
    data = json.loads(response['Body'].read().decode('utf-8'))
    return data

if __name__ == '__main__':
    bucket_name = 'enterprise-cspm'
    object_key = 'sample_data.json'
    data = fetch_data(bucket_name, object_key)
    print(data)



