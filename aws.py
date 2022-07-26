import logging
from re import S
import boto3
from botocore.exceptions import ClientError
import os
from dotenv import load_dotenv
import uuid
# from filestorage import store

load_dotenv()
# ALEX_BUCKET = "share-b-n-b"
# TAYLOR_BUCKET = "kestrelbucket"
BUCKET = os.environ['BUCKET']

def upload_file(file_name, bucket=BUCKET, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    print("bucket", bucket)

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = str(uuid.uuid4())

    s3_client = boto3.client('s3')

    try:
        response = s3_client.put_object(Body=file_name, Bucket=bucket, Key=object_name, ContentType='image/jpeg')
        image = (f'https://{bucket}.s3.amazonaws.com/{object_name}')
    except ClientError as e:
        logging.error(e)
        return False
    return image

# def download_file(file_name, bucket, object_name):
#     s3 = boto3.client('s3')
#     s3.download_file('BUCKET_NAME', 'OBJECT_NAME', 'FILE_NAME')
# # The download_fileobj method accepts a writeable file-like object. The file object must be opened in binary mode, not text mode.

#     s3 = boto3.client('s3')
#     with open('FILE_NAME', 'wb') as f:
#         s3.download_fileobj('BUCKET_NAME', 'OBJECT_NAME', f)

def show_image(bucket=BUCKET):
    s3_client = boto3.client('s3')
    public_urls = []
    try:
        for item in s3_client.list_objects(Bucket=bucket)['Contents']:
            presigned_url = s3_client.generate_presigned_url('get_object', Params = {'Bucket': bucket, 'Key': item['Key']})
            public_urls.append(presigned_url)
    except Exception as e:
        pass
    print("[INFO] : The contents inside show_image = ", public_urls)
    return public_urls


    # ExtraArgs={'ACL': 'public-read'}