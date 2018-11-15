import mimetypes
import boto.s3.connection
from boto.s3.connection import S3Connection
import os.path

root_dir = ''
access_key = ''
secret_key = ''
host = ''
port = 0
deploy_bucket_name = ''
str_len = len(root_dir)

conn = S3Connection(
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    host=host,
    port=port,
    is_secure=False,  # uncomment if you are not using ssl
    calling_format=boto.s3.connection.OrdinaryCallingFormat(),
)
# 如果没有 <deploy_bucket> 则创建一个
try:
    bucket = conn.get_bucket(deploy_bucket_name)
except:
    bucket = conn.create_bucket(deploy_bucket_name)

bucket.set_canned_acl('public-read')
# 从 root_dir 上传所有文件，并按照目录/文件名的方式组合成 key,key 的 mime type 由 headers 决定
for parent,dirnames,filenames in os.walk(root_dir):
    for filename in filenames:
        key = bucket.new_key(os.path.join(parent[str_len+1:],filename))
        contentType = mimetypes.guess_type(os.path.join(parent,filename))
        with open(os.path.join(parent, filename),'rb') as f:
            key.set_contents_from_string(f.read(), headers = {"Content-Type": contentType[0]})
        key.set_canned_acl('public-read')

