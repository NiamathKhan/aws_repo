import json

from Iam_Exception import Iam_Exception
from Set_Env import Set_Env


class Iam_Config(Set_Env):

    def __init__(self):
        super().__init__()
        global __iam_res_session
        __iam_res_session = self.session.resource("iam")

    def check_policy_arn(self, policyname, rolename=None):
        policy_arn = None
        if rolename is None:
            policy_arn = [policy.arn for policy in __iam_res_session.policies.all() if
                          policy.arn.split('/')[-1].upper() == str(policyname).upper()]
        else:
            policy_arn = [policy.arn for policy in __iam_res_session.Role(rolename).attached_policies.all() if
                          policy.arn.split("/")[-1].upper() == str(policyname).upper()]
        return policy_arn

    def check_role(self, rolename):
        role = [role.name for role in __iam_res_session.roles.all() if role.name.upper() == str(rolename).upper()]
        return role

    def create_policy(self, policyname, servicename):
        flag = False
        try:
            global __policyname, __policy_document
            __policyname = policyname
            policy_arn = self.check_policy_arn(__policyname)
            if len(policy_arn) == 0:
                self.abid_access_policy = {
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Effect": "Allow",
                            "Action": f"{servicename}:*",
                            "Resource": "*"
                        }
                    ]
                }
                __policy_document = json.dumps(self.abid_access_policy)
                __iam_res_session.create_policy(PolicyName=__policyname, PolicyDocument=__policy_document)
            policy_arn = self.check_policy_arn(__policyname)
            if len(policy_arn) == 0:
                raise Iam_Exception(f"policy {__policyname} could not create\n")
            else:
                flag = True
        except Iam_Exception as e:
            print(e.message)
            return flag
        except Exception as e:
            print(e)
            return flag

    def create_role(self, rolename, servicename):
        flag = False
        try:
            role = self.check_role(rolename)
            if len(role) == 0:
                path = "/"
                rolename = rolename
                description = f"{servicename} role managed by developer : Niamath"
                role_policy = {
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Sid": "",
                            "Effect": "Allow",
                            "Principal": {
                                "Service": f"{servicename}.amazonaws.com"
                            },
                            "Action": "sts:AssumeRole"
                        }
                    ]
                }
                tags = [
                    {
                        'Key': 'Name',
                        'Value': f'{servicename} role managed by developer : Niamath'
                    }
                ]
                response = __iam_res_session.create_role(
                    Path=path,
                    RoleName=rolename,
                    AssumeRolePolicyDocument=json.dumps(role_policy),
                    Description=description,
                    MaxSessionDuration=3600,
                    Tags=tags
                )
            role = self.check_role(rolename)
            if len(role) == 0:
                raise Iam_Exception(f"role {rolename} could not create\n")
            else:
                flag = True
            return flag
        except Iam_Exception as e:
            print(e.message)
            return flag
        except Exception as e:
            print(e)
            return flag

    def attach_policy_to_role(self, policyname, rolename):
        flag = False
        try:
            attached_policy_arn = self.check_policy_arn(policyname, rolename=rolename)
            if len(attached_policy_arn) == 0:
                policy_arn = [policy.arn for policy in __iam_res_session.policies.all() if
                              policy.arn.split('/')[-1].upper() == str(policyname).upper()]
                iam_client_session = __iam_res_session.meta.client
                iam_client_session.attach_role_policy(PolicyArn=policy_arn[0], RoleName=rolename)
            attached_policy_arn = self.check_policy_arn(policyname, rolename=rolename)
            if len(attached_policy_arn) == 0:
                raise Iam_Exception(f"policy {policyname} could not be attached to role {rolename}\n")
            else:
                flag = True
            return flag
        except Iam_Exception as e:
            print(e.message)
            return flag
        except Exception as e:
            print(e)
            return flag


'''if __name__ == "__main__":
    role_name,role_service,policy_name,policy_service = input(f"please enter role_name,role_service and policy_name,policy_service seperated by , \n").split(",")
    o = Iam_Config()
    o.create_policy(policy_name,policy_service)
    o.create_role(role_name,role_service)
    o.attach_policy_to_role(policy_name,role_name)'''
