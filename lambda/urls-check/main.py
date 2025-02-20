import json
import os
import re

import boto3
import requests
from bs4 import BeautifulSoup

s3_client = boto3.client("s3")
bucket_name = os.environ["BUCKET_NAME"]


def load_from_s3(file_name):
    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=file_name)
        file_content = response["Body"].read().decode("utf-8")
        return json.loads(file_content)
    except Exception as e:
        print(e)
        return []

def save_into_s3(file_name, json_data):
    s3_client.put_object(
        Bucket=bucket_name,
        Key=file_name,
        Body=json_data,
        ContentType="application/json"
    )

def handler(event, context):
    processed_file_name = os.environ["FILE_NAME"]
    rtbf_url = os.environ["RTBF_URL"]

    response = requests.get(rtbf_url, timeout=10)
    image_regex = re.compile(r".*[a-zA-Z]$", re.IGNORECASE)
    if response.status_code == 200:
        to_process_filename = "to_process.json"
        return extract_urls(
            response, image_regex, processed_file_name, to_process_filename
        )
    print(f"Failed to fetch XML: {response.status_code}")
    return None


def extract_urls(response, image_regex, processed_file_name, to_process_filename):
    soup = BeautifulSoup(response.content, "xml")
    urls = [loc.text.strip() for loc in soup.find_all("loc") if not image_regex.match(loc.text.strip())]
    processed_url = load_from_s3(processed_file_name)
    to_process_url = set(urls).difference(set(processed_url))
    save_into_s3(to_process_filename, json.dumps(to_process_url))
    return {"statuscode": 200, "#urls": len(to_process_url),"urls": json.dumps({"urls": to_process_url})}
