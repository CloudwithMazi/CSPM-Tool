import boto3 
import json 

s3_client = boto3.client('s3')

bucket_name = 'enterprise-cspm'
object_key = 'sample_data.json'

response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
data = json.loads(response['Body'].read())

print(json.dumps(data, indent=4))
