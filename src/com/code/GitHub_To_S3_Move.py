import os,git,logging,shutil,stat
from botocore.exceptions import ClientError

logging.basicConfig(filename='./aws_automation_logger.log',level=logging.FATAL,filemode='a+',format='%(name)s - %(timestamp)s - %(levelname)s - %(message)s')
os.environ['properties_file'] = os.path.abspath('..\\..\\..\\resources\\config.properties')

class Env_Exception(Exception):
    def __init__(self,message):
        self.message = message

class Set_Env(object):
    def __init__(self):
        self.session = None
        try:
            properties_file = os.environ['properties_file']
            if os.stat(properties_file).st_size != 0:
                with open(properties_file) as p_f:
                    for lines in p_f.readlines():
                        k_v = lines.strip('\n').split('=')
                        os.environ[k_v[0]] = k_v[1]
                self.session = boto3.Session()
            else:
                raise Env_Exception(f'{properties_file} is empty')
        except Env_Exception as e:
            logging.fatal(e)
        except Exception as e:
            logging.fatal(e)

class GitHub_To_S3_Move(Set_Env):
    def __init__(self):
        super().__init__()
        global __s3_session
        __s3_session = self.session.resource('s3')
    def copy_github_to_s3(self,git_url,s3_bucket_name):
        try:
            os.mkdir('collect_from_github')
            root_path = './/collect_from_github/'
            git.Git(root_path).clone(git_url)
            bucket = __s3_session.Bucket(s3_bucket_name)
            for path,subdir,files in os.walk(root_path):
                path = path.replace('\\','/')
                dir_name = path.replace(root_path,'')
                for file in files:
                    filepath = os.path.join(path,file).replace('\\','/')
                    bucket.upload_file(os.path.join(path,file),dir_name+'/'+file)
                    os.chmod(filepath,stat.S_IWRITE)
            os.system(f'attrib -r -s -h {root_path}')
            shutil.rmtree(root_path,True)
        except ClientError as e:
            logging.fatal(e)
        except Exception as e:
            logging.fatal(e)
if __name__ == '__main__':
    git_url,s3_bucket_name = input(f'enter git_url and s3_bucketname seperated by , \n').split(',')
    GitHub_To_S3_Move().copy_github_to_s3(git_url,s3_bucket_name)
