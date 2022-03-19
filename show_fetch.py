import requests
import json
import boto3
from botocore.exceptions import ClientError
from pprint import pprint

# Method to write show JSON data to DynamoDB
def get_show(mal_id):
    # table = dynamodb.Table('shows_jikan')
    table = dynamodb.Table('shows_mal')

    try:
        response = table.get_item(Key={'mal_id': mal_id})
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return response['title']

dynamodb = boto3.resource('dynamodb')
mal_id = 1

movie = get_show(mal_id)

if movie:
    print("Get movie succeeded:")
    pprint(movie, sort_dicts=False)
