import html
import json
import os
import re
from datetime import datetime

import boto3
import requests
from bs4 import BeautifulSoup

s3_client = boto3.client("s3")
bucket_name = os.environ["BUCKET_NAME"]
dynamodb = boto3.resource('dynamodb')


def upload_to_dynamodb(table_name, url_id, url, json_data):
    table = dynamodb.Table(table_name)
    d = datetime.now()

    try:
        return table.put_item(
            Item={
                'ID': url_id,
                'URL': url,
                'Title': html.unescape(json_data['headline']),
                'Text': html.unescape(json_data['articleBody']),
                'PublishDate': json_data['datePublished'],
                'ModifiedDate': json_data['dateModified'],
                'JournalistName': json_data['author']['name'],
                'ExtractionDate': f"{d.day}/{d.month}/{d.year}",
            }
        )
    except Exception as e:
        print(f"Error uploading to DynamoDB: {str(e)}")
        raise e


def get_article(url, table_name):
    html_content = requests.get(url).text
    soup = BeautifulSoup(html_content, 'html.parser')
    json_ld_scripts = soup.find_all('script', type='application/ld+json')
    for script in json_ld_scripts:
        try:
            json_data = json.loads(script.string)
            if json_data.get('@type') == 'NewsArticle' and 'datePublished' in json_data:
                url_id = re.split("-", url)[-1]
                upload_to_dynamodb(table_name, url_id, url, json_data)

        except json.JSONDecodeError:
            continue
    return {}


def handler(event, context):
    url = event["url"]
    return get_article(url, event["table_name"]) != {}
