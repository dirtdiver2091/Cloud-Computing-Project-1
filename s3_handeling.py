import config
import boto3

bucket_name = config.bucket_name
print(bucket_name)

client = boto3.client('s3', aws_access_key_id = config.api_key, aws_secret_access_key = config.api_secret)

def upload(file_name, object_name):

	response = client.upload_file(file_name, bucket_name, object_name, ExtraArgs={'ACL':'public-read'})
	return response


def download(bucket, file_name):
	print(file_name)
	print(f'./{file_name}')
	response = client.download_file(bucket_name, file_name, f'./media/{file_name}')
	return response

def list_content():
    content = []
    try:
        for item in client.list_objects(Bucket=bucket_name)['Contents']:
            content.append(item)
    except KeyError:
        pass
    print(content)
    return content