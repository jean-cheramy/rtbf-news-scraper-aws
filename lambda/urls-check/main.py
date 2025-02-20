import requests
import re
from bs4 import BeautifulSoup


import json


def handler(event, context):
    url = "https://www.rtbf.be/site-map/articles5000.xml"
    response = requests.get(url, timeout=10)
    image_regex = re.compile(r".*[a-zA-Z]$", re.IGNORECASE)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "xml")
        urls = [loc.text.strip() for loc in soup.find_all("loc") if not image_regex.match(loc.text.strip())]
        return {"statuscode": 200, "body": json.dumps({"urls": urls})}
    else:
        print(f"Failed to fetch XML: {response.status_code}")
        return None
