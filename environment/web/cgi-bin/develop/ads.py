import os
import json
import boto3

from launcher.rlauncher import RLauncher

class AdsLauncher(RLauncher):
    def __init__(self):
        super(AdsLauncher, self).__init__()
    def initialize(self):
        os.environ['AWS_DEFAULT_REGION'] = 'ap-northeast-1'
        return 0
    def run(self):
        if self.isGet():
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('gcs-dynamodb-pretest')
            ret = table.get_item(
                Key = {
                    'user_id': 1,
                }
            )
            item = ret['Item']
            print(item)
        else:
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('gcs-dynamodb-pretest')
            item = {
                'user_id': 5,
                'created_datetime': 1596361016
            }
            table.put_item(Item=item)
        return 0
    def finalize(self):
        return 0
