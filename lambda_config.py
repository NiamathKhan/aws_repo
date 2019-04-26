import os,boto3
from Iam_Config import Iam_Config
from Set_Env import Set_Env


class TestDev(Set_Env):
    def __init__(self, policy_name, policy_service, role_name, role_service):
        super().__init__()
        global __role_name, __role_service, __policy_name, __policy_service
        __role_name = role_name
        __role_service = role_service
        __policy_name = policy_name
        __policy_service = policy_service
        self.lambda_session = self.session.client('lambda', os.environ['region_name'])

    def create_function(self,functionname):
        iam_o = Iam_Config()
        flag = False
        iam_o.create_policy(policyname=__policy_name, servicename=__policy_service)
        iam_o.create_role(rolename=__role_name, servicename=__role_service)
        iam_o.attach_policy_to_role(policyname=__policy_name, rolename=__role_name)
        roles = iam_o.check_role(rolename=__role_name)
        if len(roles) != 0:
            with open('C:\\Users\\nkhan\\PycharmProjects\\aws_practice\\com\\practice\\lambda_function.zip', 'rb') as z_f:
                zipped_code = z_f.read()
            role = roles[0]
            fun_response=self.lambda_session.create_function(
                FunctionName=functionname,
                Runtime='python3.7',
                Role=self.session.client('iam').get_role(RoleName=role)['Role']['Arn'],
                Handler='lambda_function.handler',
                Code=dict(ZipFile=zipped_code),
                Timeout=300,
            )
            fn_arn = fun_response['FunctionArn']
            name = f"{functionname}-Trigger"
            self.lambda_session.add_permission(
                FunctionName = functionname,
                StatementId = f"{name}-Event",
                Action = 'lambda:InvokeFunction',
                Principal = 's3.amazonaws.com',
                SourceArn = 'arn:aws:s3:::abidkhan-versioned-bucket02'
            )

    def add_s3_as_trigger(self,functionname,bucketname):
        response = self.session.client('s3',os.environ['region_name']).put_bucket_notification_configuration(
            Bucket=bucketname,
            NotificationConfiguration={
                'LambdaFunctionConfigurations': [
                    {
                        'Id': 'string',
                        'LambdaFunctionArn': self.lambda_session.get_function(FunctionName = functionname)['Configuration']['FunctionArn'],
                        'Events': [
                            's3:ObjectCreated:*'
                        ]
                    }
                ]
            }
        )
if __name__ == "__main__":
    policyname,policyservice,rolename,roleservice = input(f"please enter policyname,policyservice,rolename,roleservice seperated by , \n").split(',')
    o = TestDev(policyname,policyservice,rolename,roleservice)
    functionname = input(f"please enter function name \n")
    o.create_function(functionname)
    o.add_s3_as_trigger(functionname=functionname,bucketname='abidkhan-versioned-bucket02')













