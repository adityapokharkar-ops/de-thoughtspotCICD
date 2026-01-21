import pandas as pd
import os
import requests
import json
import csv
import logging

# --------------------------------------------------
# BASIC LOGGER CONFIGURATION
# --------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("commit_debug.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# --------------------------------------------------
# AUTHENTICATION
# --------------------------------------------------
def auth_call():
    auth_url = 'https://ts.dev.simpplr.xyz/api/rest/2.0/auth/token/full'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    payload = {
        "username": "aditya.pokharkar@simpplr.com",
        "auto_create": False,
        "password": "Planet@107",
        "secret_key": "34ecbf78-0641-4c41-b333-0b972b3eb704",
        "validity_time_in_sec": 600
    }

    try:
        response = requests.post(auth_url, headers=headers, data=json.dumps(payload))
        logger.info("Auth API called")
        logger.info(f"Auth response status : {response.status_code}")
        logger.debug(f"Auth response body  : {response.text}")
        response.raise_for_status()
        logger.info("Successfully logged in")
    except requests.exceptions.RequestException as e:
        logger.error("Login failed")
        logger.error(f"Response body : {response.text}")
        logger.exception(e)
        raise

    json_text = response.json()
    Bearer_token = json_text['token']
    logger.info("Bearer token received")
    logger.info("===================================================")

    return Bearer_token


Bearer_token = auth_call()

# --------------------------------------------------
# COMMIT CALL
# --------------------------------------------------
def commit_call(Bearer_token):

    metadata_search_url = 'https://ts.dev.simpplr.xyz/api/rest/2.0/metadata/search'
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
        "tag_identifiers": ["test"]
    }

    # ---------------- METADATA SEARCH ----------------
    try:
        response = requests.post(
            metadata_search_url,
            headers=headers,
            data=json.dumps(payload_commit)
        )
        logger.info("Metadata search API called")
        logger.info(f"Metadata search status : {response.status_code}")
        logger.debug(f"Metadata search body  : {response.text}")
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error("Metadata search failed")
        logger.error(f"Response body : {response.text}")
        logger.exception(e)
        raise

    json_text = response.json()
    logger.info(f"Number of objects found : {len(json_text)}")

    # ---------------- STORE METADATA ----------------
    metadata_id = []
    metadata_name = []
    metadata_type = []

    for i in json_text:
        metadata_id.append(i['metadata_id'])
        metadata_name.append(i['metadata_name'])
        metadata_type.append(i['metadata_type'])

    df = pd.DataFrame({
        'metadata_id': metadata_id,
        'metadata_name': metadata_name,
        'metadata_type': metadata_type
    })

    df.to_csv('metadata_information.csv', index=False)
    logger.info("Metadata CSV created")

    # ---------------- COMMIT LOOP ----------------
    for i in range(len(df)):
        guid = df['metadata_id'][i]

        payload = {
            "metadata": [
                {"identifier": guid}
            ],
            "delete_aware": True,
            "branch_name": "test",
            "comment": "TMLs committed to test branch"
        }

        try:
            response = requests.post(
                commit_url,
                headers=headers,
                data=json.dumps(payload)
            )

            logger.info("--------------------------------------------------")
            logger.info(f"Committing GUID       : {guid}")
            logger.info(f"Object Type          : {df['metadata_type'][i]}")
            logger.info(f"Object Name          : {df['metadata_name'][i]}")
            logger.info(f"Commit status code   : {response.status_code}")
            logger.info(f"Commit response body : {response.text}")

            response.raise_for_status()

            logger.info("COMMIT SUCCESS")

        except requests.exceptions.RequestException as e:
            logger.error("COMMIT FAILED")
            logger.error(f"GUID                : {guid}")
            logger.error(f"Status Code         : {response.status_code}")
            logger.error(f"Response Body       : {response.text}")
            logger.exception(e)

    logger.info("===================================================")
    logger.info("Commit process completed")


commit_call(Bearer_token)
