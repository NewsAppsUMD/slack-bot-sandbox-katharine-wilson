import os
import json
from datetime import datetime
import requests
from slack import WebClient
from slack.errors import SlackApiError

slack_token = os.environ.get('SLACK_API_TOKEN')
congress_api_key = "aKfCNxb80QWUylo4eaneyGasY8J4LREvxqkoRYy4"

client = WebClient(token=slack_token)
url = f"https://api.congress.gov/v3/committee-report/119/hrpt?api_key={congress_api_key}&format=json"

r = requests.get(url)

results = r.json()

first_result = results['reports'][0]

###### Fixing the url
dispay_url = f"https://www.congress.gov/congressional-report/{first_result['congress']}-congress/house-report/{first_result['number']}"

##### Fixing the date format
display_date = datetime.strptime(first_result['updateDate'], '%Y-%m-%dT%H:%M:%SZ')
formatted_date = display_date.strftime('%B %-d, %Y at %-I:%M%p')

sentence = f"On {formatted_date}, the {first_result['chamber']} published {first_result['citation']}, which is available at {dispay_url}"

msg = sentence

try:
    response = client.chat_postMessage(
        channel="slack-bots",
        text=msg,
        unfurl_links=True, 
        unfurl_media=True
    )
    print("success!")
except SlackApiError as e:
    assert e.response["ok"] is False
    assert e.response["error"]
    print(f"Got an error: {e.response['error']}")