import os,boto3
root_path = 'D:\\collect_from_github'
properties_file = os.environ['properties_path']
with open(properties_file) as p_f:
    for line in p_f.readlines():
        k_v = line.strip('\n').split('=')
        os.environ[k_v[0]] = k_v[1]

bucket = boto3.resource('s3').Bucket('abidkhan-versioned-bucket02')
for path,subdirs,files in os.walk(root_path):
    path = path.replace('\\','/')
    dir_name =path.replace(root_path,'')
    for file in files:
        bucket.upload_file(os.path.join(path,file),dir_name+'/'+file)
print("done the job !")
