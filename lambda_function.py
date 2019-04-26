import boto3


def handler(event, context):
    try:
        sns_session = boto3.client('sns')
        topic_name = 'abid_test_topic_test10'
        message = "Hello This is a test mail from Niamath Khan"
        topic_arn = [topic['TopicArn'] for topic in sns_session.list_topics()['Topics'] if
                     topic['TopicArn'].split(':')[-1].upper() == topic_name.upper()]
        sns_session.publish(Message=message, TopicArn=topic_arn)
    except Exception as e:
        print(e)
