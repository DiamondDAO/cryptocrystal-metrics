import requests
from datetime import datetime, timedelta
import time
import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from decimal import Decimal
import numpy as np
from github import Github
import os
import argparse
from pathlib import Path
import pandas as pd
import json
from util.github_util import update_type_table_repo
from util.misc_util import clean_type_entries, parse_iso_date
from util.aws_util import update_type_table

dynamodb = boto3.resource("dynamodb")
type_table = dynamodb.Table("crystal_type_table")

event_url = "https://api.opensea.io/api/v1/events"
event_querystring = {
    "collection_slug": "cryptocrystal",
    "event_type": "successful",
    "only_opensea": "false",
    "offset": "0",
    "limit": "50",
}

asset_url = "https://api.opensea.io/api/v1/asset/0xcfbc9103362aec4ce3089f155c2da2eea1cb7602/"
asset_querystring = {"order_direction": "desc", "offset": "0", "limit": "20", "collection": "cryptocrystal"}

headers = {"Accept": "application/json"}
main_data_path = Path("/home/ubuntu/dat/cryptocrystal/last_date_listener.txt")

if not main_data_path.is_file():
    main_data_path = Path("/users/rohan/diamond/dat/cryptocrystal/last_date_listener.txt")

with open(main_data_path, "r") as file:
    last_date = parse_iso_date(file.readline().replace("\n", ""))
    new_changes = int(file.readline().replace("\n", ""))

response = type_table.scan()
data = response["Items"]

while "LastEvaluatedKey" in response:
    response = type_table.scan(ExclusiveStartKey=response["LastEvaluatedKey"])
    data.extend(response["Items"])

rarity_list, crystal_types = clean_type_entries(data)
for idx, item in enumerate(crystal_types):
    crystal_types[idx]["last_sale"] = None

crystal_type_df = pd.DataFrame(crystal_types)
all_types = list(crystal_type_df["crystal_type"])


offset = 0
event_querystring["occurred_after"] = last_date.isoformat()
event_querystring["offset"] = offset
response = requests.request("GET", event_url, headers=headers, params=event_querystring).json()
events = response.get("asset_events", [])
if not events:
    print("No events this time")
else:
    while True:
        offset += 50
        event_querystring["offset"] = offset
        response = requests.request("GET", event_url, headers=headers, params=event_querystring).json()
        more_events = response.get("asset_events", [])
        if not more_events:
            break
        events.extend(more_events)
    print(len(events))
    for event in events:
        current_token_id = event["asset"]["token_id"]
        crystal_type = 0
        current_asset_url = asset_url + current_token_id + "/"
        asset = requests.request("GET", current_asset_url, headers=headers, params=asset_querystring).json()
        if not asset:
            continue
        item = asset
        trait_test = item.get("traits", [])
        if not trait_test:
            continue
        for trait in item["traits"]:
            if trait["trait_type"] == "kind":
                crystal_type = trait["value"]
            elif trait["trait_type"] == "weight":
                crystal_weight = Decimal(int(trait["value"]))
        if not crystal_type:
            continue
        if crystal_type not in all_types:
            continue
        current_last_sale = {}
        current_last_sale["timestamp"] = event["transaction"]["timestamp"]
        current_last_sale["price"] = Decimal(int(event["total_price"])) / Decimal((10 ** 18))
        current_last_sale["weight"] = crystal_weight

        update_type_table_response = update_type_table(type_table, crystal_type, current_last_sale)
        if update_type_table_response:
            new_changes += 1
            print(f"{crystal_type} Updated!")

    if new_changes >= 5:
        aws_api_url = "https://quf1ev88a9.execute-api.us-east-2.amazonaws.com/default/return_crystal_types"
        request_payload = {"type_table": "true", "type": "none", "all_types": "false"}
        r = requests.post(
            aws_api_url,
            data=json.dumps(request_payload),
            headers={"Content-Type": "application/json", "origin": "null"},
        )
        new_table_html = json.loads(r.content)["new_type_table"]
        g = Github(os.environ["GITHUB_ACCESS_TOKEN"])
        repo = g.get_repo("diamonddao/cryptocrystal-metrics")
        commit_response = update_type_table_repo(repo, "docs/index.html", new_table_html)
        print(commit_response)
        new_changes = 0

if last_date + timedelta(days=1) < datetime.now():
    last_date = last_date + timedelta(days=1)

with open(main_data_path, "w") as file:
    file.write(last_date.isoformat())
    file.write("\n")
    file.write(str(new_changes))
