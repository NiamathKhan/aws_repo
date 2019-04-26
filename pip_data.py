from botocore.exceptions import ClientError
from File_IO_Exception import S3_Exception
from Set_Env import Set_Env

''': type : pyboto3.s3'''


class Create_Bucket(Set_Env):
    def __init__(self, bucketname, objectname):
        super().__init__()
        global __bucketname, __objectname
        __bucketname = bucketname
        __objectname = objectname

    def create_bucket(self):
        flag = False
        try:
            s3_res_session = self.session.resource("s3")
            bucket_exists = [bucket for bucket in s3_res_session.buckets.all() if bucket.name == __bucketname]
            if len(bucket_exists) != 0:
                flag = True
            if len(bucket_exists) == 0:
                s3_res_session.create_bucket(Bucket=__bucketname)
                v_b = s3_res_session.BucketVersioning(__bucketname)  # enable BucketVersioning
                v_b.enable()
                flag = True
            bucket_exists = s3_res_session.meta.client.head_bucket(Bucket=__bucketname)
            return flag
        except ClientError as e:
            error_code = ClientError.response['Error']['Code']
            if error_code == 403:
                print("Forbidden Bucket ! you are not allowed to access it !")
            elif error_code == 404:
                print("Bucket does not exists !")
            else:
                print(f"some other exception while creating bucket {e}")
            return flag
        except Exception as e:
            print(e)
            return flag

    def upload_object(self):
        flag = False
        try:
            s3_res_session = self.session.resource("s3")
            object_name = __objectname.split("\\")[-1]
            # print(f"done till here ! {__objectname},{__bucketname},{object_name}\n")
            # s3_res_session.meta.client.upload_file(__objectname,__bucketname,object_name)
            bucket = s3_res_session.Bucket(__bucketname)
            bucket.upload_file(__objectname, object_name)
            # print("done till here !")
            object_created = [object for object in bucket.objects.all() if object.key == object_name]
            if len(object_created) == 0:
                raise S3_Exception(f"object {object_name} could not create into bucket {__bucketname}\n")
            else:
                flag = True
            return flag
        except S3_Exception as e:
            print(e.message)
            return flag
        except Exception as e:
            print(e)
            return flag
