import numpy as np
import pandas as pd
import os
import requests
import json
import csv
# Authentication url for Deploy API call
def deploy_auth():
    deploy_auth_url = 'https://ts.dev.simpplr.xyz/api/rest/2.0/auth/token/full'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    payload = {
        "username": "aditya.pokharkar@simpplr.com",
        "auto_create": False,
        "password": "Planet@107",
        "secret_key": "ae818922-6b35-410f-a68d-7cef4c4b7fa8"
    }
    try:
        response = requests.post(deploy_auth_url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Raises error if status >= 400
        print(f"✅_check_mark: Successfully Logged_in")
    except requests.exceptions.RequestException as e:
        print(f"❌: Login Failed: {e}")
    # Store the Bearer Token fro next API calls
    json_text=response.json()
    json_text['token']
    Bearer_token = json_text['token']
    print("==========================================")
    return Bearer_token
Bearer_token = deploy_auth()

# This url deploy all the TML files from Github(Deploy branch) to your environment
def deploy_call(Bearer_token):
    deploy_url = 'https://ts.dev.simpplr.xyz/api/rest/2.0/vcs/git/commits/deploy'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {Bearer_token}'
    }
    payload = {
        "branch_name": "perf",
        "deploy_type": "DELTA",
        "deploy_policy": "ALL_OR_NONE"
    }
    try:
        response = requests.post(deploy_url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Raises error if status >= 400
        print(f"✅_check_mark: Successfully Deployed")
    except requests.exceptions.RequestException as e:
        print(f"❌: Deploy Failed: {e}")
    return None
deploy_call = deploy_call(Bearer_token)











