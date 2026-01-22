import numpy as np
import pandas as pd
import os
import requests
import json
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
    deploy_auth_url = "https://ts.dev.simpplr.xyz/api/rest/2.0/auth/token/full"

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    payload = {
        "username": "aditya.pokharkar@simpplr.com",
        "auto_create": False,
        "password": "Planet@107",
        "secret_key": "4fa24e4b-00af-4b1e-920c-62f818197ab6"
    }

    try:
        response = requests.post(
            deploy_auth_url,
            headers=headers,
            data=json.dumps(payload)
        )

        logger.info("Auth API called")
        logger.info(f"Auth status code : {response.status_code}")
        response.raise_for_status()

    except requests.exceptions.RequestException as e:
        logger.error("Authentication failed")
        logger.error(response.text)
        raise

    token = response.json()["token"]
    logger.info("Bearer token received")
    logger.info("===================================")

    return token


# --------------------------------------------------
# DEPLOY FUNCTION
# --------------------------------------------------
def deploy_call(Bearer_token):

    deploy_url = "https://ts.dev.simpplr.xyz/api/rest/2.0/vcs/git/commits/deploy"

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {Bearer_token}"
    }

    # --------------------------------------------------
    # READ VALUES FROM GITHUB ACTIONS
    # --------------------------------------------------
    deploy_type = os.getenv("DEPLOY_TYPE", "DELTA")
    deploy_policy = os.getenv("DEPLOY_POLICY", "ALL_OR_NONE")

    # --------------------------------------------------
    # VALIDATION (IMPORTANT)
    # --------------------------------------------------
    if deploy_type not in ["DELTA", "FULL"]:
        raise ValueError("DEPLOY_TYPE must be DELTA or FULL")

    if deploy_policy not in ["ALL_OR_NONE", "PARTIAL"]:
        raise ValueError("DEPLOY_POLICY must be ALL_OR_NONE or PARTIAL")

    # --------------------------------------------------
    # LOG CONFIG
    # --------------------------------------------------
    logger.info("========== DEPLOY CONFIG ==========")
    logger.info("Branch Name   : migration")
    logger.info(f"Deploy Type   : {deploy_type}")
    logger.info(f"Deploy Policy : {deploy_policy}")
    logger.info("===================================")

    # --------------------------------------------------
    # DEPLOY PAYLOAD
    # --------------------------------------------------
    payload = {
        "branch_name": "migration",
        "deploy_type": deploy_type,
        "deploy_policy": deploy_policy
    }

    try:
        response = requests.post(
            deploy_url,
            headers=headers,
            data=json.dumps(payload)
        )

        logger.info(f"Deploy status code   : {response.status_code}")
        logger.info(f"Deploy response body : {response.text}")

        response.raise_for_status()
        logger.info("DEPLOY SUCCESSFUL ✅")

    except requests.exceptions.RequestException as e:
        logger.error("DEPLOY FAILED ❌")
        logger.error(response.text)
        raise

    logger.info("===================================")


# --------------------------------------------------
# MAIN
# --------------------------------------------------
if __name__ == "__main__":
    token = deploy_auth()
    deploy_call(token)
