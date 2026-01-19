import numpy as np
import pandas as pd
import os
import requests
import json
import csv
# Authentication url for Commit API Call
def auth_call ():
    auth_url = 'https://ts.dev.simpplr.xyz/api/rest/2.0/auth/token/full'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    payload = {
        "username": "aditya.pokharkar@simpplr.com",
        "auto_create": False,
        "password": "Planet@107",
        "secret_key": "34ecbf78-0641-4c41-b333-0b972b3eb704"
    }
    
    try:
        response = requests.post(auth_url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Raises error if status >= 400
        print(f"✅: Successfully Logged_in")
    except requests.exceptions.RequestException as e:
        print(f"❌: Login Failed: {e}")
    # Store the Bearer Token for next API calls
    json_text=response.json()
    json_text['token']
    Bearer_token = json_text['token']
    print("===================================================")
    return Bearer_token
Bearer_token = auth_call ()

def commit_call(Bearer_token):
    # Metadata Search URL with TAG_IDENTIFIER
    metadata_search_url = 'https://ts.dev.simpplr.xyz/api/rest/2.0/metadata/search'
    # Version Control API url for COMMIT
    commit_url = 'https://ts.dev.simpplr.xyz/api/rest/2.0/vcs/git/branches/commit'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {Bearer_token}'
    }
    payload_commit = {
            "record_offset": 0,
            "record_size": 10000,
        "metadata": [
            {"type": "LIVEBOARD"},
            {"type": "ANSWER"},
            {"type": "LOGICAL_TABLE"},
            {"type": "CONNECTION"},
            {"type": "LOGICAL_RELATIONSHIP"}
        ],
            "tag_identifiers": ["analytics"],
    }
    try:
        response = requests.post(metadata_search_url, headers=headers, data=json.dumps(payload_commit))
        response.raise_for_status()  # Raises error if status >= 400
        print(f"✅: Success for Metadata_Search API call")
    except requests.exceptions.RequestException as e:
        print(f"❌: Failure for Metadata_Search API call: {e}")
    # Store the Response in a variable
    json_text=response.json()
    # Create an empty list to store metadata_information
    metadata_id = []
    metadata_name = []
    metadata_type = []
    for i in json_text:
        metadata_id.append(i['metadata_id'])
        metadata_name.append(i['metadata_name'])
        metadata_type.append(i['metadata_type'])
    # Create a dataframe and a CSV file to store the metadata information
    df = pd.DataFrame()
    df['metadata_id'] = metadata_id
    df['metadata_name'] = metadata_name
    df['metadata_type'] = metadata_type
    df.to_csv('metadata_information.csv')
    # Read GUIDs from CSV
    metadata_df = pd.read_csv('metadata_information.csv')
    metadata_df.drop(columns=['Unnamed: 0'] , inplace=True)
    for i in range(len(metadata_df)) :
        guid = df['metadata_id'][i]
        payload = {
            "metadata": [
                {
                    "identifier": guid
                }
            ],
            "delete_aware": True,
            "branch_name": "test",
            "comment": "TMLs committed to test branch"
        }
        try:
            response = requests.post(commit_url, headers=headers, data=json.dumps(payload))
            response.raise_for_status()  # Raises error if status >= 400
            print(f"✅: Success for GUID {guid} , 'metadata_type': {df['metadata_type'][i]} , 'metadata_name': {df['metadata_name'][i]}" )
        except requests.exceptions.RequestException as e:
            print(e)
            print(f"❌: Failure for GUID {guid}, 'metadata_type': {df['metadata_type'][i]}, 'metadata_name': {df['metadata_name'][i]} — Error: {e}")
    return None
commit_call= commit_call(Bearer_token)


