import os
import re

import boto3
import requests

s3_client = boto3.client("s3")
bucket_name = os.environ["BUCKET_NAME"]


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