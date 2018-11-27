# upload_files_to_radosgw
Upload all files from a local directory to Ceph Radosgw

## Parameters Information
parser.add_argument('--root_dir',required=True,help="path to static resource on local machine")
parser.add_argument('--access_key',required=True,help="Ceph OBJ Storage Access Key")
parser.add_argument('--secret_key',required=True,help="Ceph OBJ Storage Secret Key")
parser.add_argument('--host',required=True,help="Ceph OBJ Storage Endpoint host")
parser.add_argument('--port',required=True,help="Ceph OBJ Storage Endpoint port",default=8080)
parser.add_argument('--deploy_bucket_name',required=True,help="Ceph OBJ Storage Bucket Name")
