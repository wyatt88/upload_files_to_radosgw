import mimetypes
import boto.s3.connection
from boto.s3.connection import S3Connection
import os.path
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--root_dir',required=True,help="path to static resource on local machine")
parser.add_argument('--access_key',required=True,help="Ceph OBJ Storage Access Key")
parser.add_argument('--secret_key',required=True,help="Ceph OBJ Storage Secret Key")
parser.add_argument('--host',required=True,help="Ceph OBJ Storage Endpoint host")
parser.add_argument('--port',required=True,help="Ceph OBJ Storage Endpoint port",default=8080)
parser.add_argument('--deploy_bucket_name',required=True,help="Ceph OBJ Storage Bucket Name")

parser.print_help()
args = parser.parse_args()

# root_dir = ''
# access_key = ''
# secret_key = ''
# host = ''
# port = 0
# deploy_bucket_name = ''

str_len = len(args.root_dir)

conn = S3Connection(
    aws_access_key_id=args.access_key,
    aws_secret_access_key=args.secret_key,
    host=args.host,
    port=int(args.port),
    is_secure=False,  # uncomment if you are not using ssl
    calling_format=boto.s3.connection.OrdinaryCallingFormat(),
)
# if have no bucket <deploy_bucket> , create new one
try:
    bucket = conn.get_bucket(args.deploy_bucket_name)
except:
    bucket = conn.create_bucket(args.deploy_bucket_name)

bucket.set_canned_acl('public-read')

for parent,dirnames,filenames in os.walk(args.root_dir):
    for filename in filenames:
        key = bucket.new_key(os.path.join(parent[str_len+1:],filename))
        contentType = mimetypes.guess_type(os.path.join(parent,filename))
        with open(os.path.join(parent, filename),'rb') as f:
            key.set_contents_from_string(f.read(), headers = {"Content-Type": contentType[0]})
        key.set_canned_acl('public-read')

