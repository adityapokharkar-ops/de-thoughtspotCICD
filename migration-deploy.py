import numpy as np
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
        logging.FileHandler("deploy_debug.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# --------------------------------------------------
# AUTHENTICATION
# --------------------------------------------------
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
        "secret_key": "511464d0-ef88-48d7-895c-69d422bdcc9c"
    }

    try:
        response = requests.post(
            deploy_auth_url,
            headers=headers,
            data=json.dumps(payload)
        )

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


Bearer_token = deploy_auth()

# --------------------------------------------------
# DEPLOY CALL
# --------------------------------------------------
def deploy_call(Bearer_token):

    deploy_url = 'https://ts.dev.simpplr.xyz/api/rest/2.0/vcs/git/commits/deploy'

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {Bearer_token}'
    }

    payload = {
        "branch_name": "migration",
        "deploy_type": "DELTA",
        "deploy_policy": "ALL_OR_NONE"
    }

    try:
        response = requests.post(
            deploy_url,
            headers=headers,
            data=json.dumps(payload)
        )

        logger.info("Deploy API called")
        logger.info(f"Deploy branch        : migration")
        logger.info(f"Deploy status code   : {response.status_code}")
        logger.info(f"Deploy response body : {response.text}")

        response.raise_for_status()
        logger.info("DEPLOY SUCCESSFUL ✅")

    except requests.exceptions.RequestException as e:
        logger.error("DEPLOY FAILED ❌")
        logger.error(f"Status Code   : {response.status_code}")
        logger.error(f"Response Body : {response.text}")
        logger.exception(e)
        raise

    logger.info("===================================================")


deploy_call(Bearer_token)
