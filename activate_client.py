import requests
import hashlib
import uuid
import json
import os


API_URL = "http://127.0.0.1:8000"

SESSION_FILE = "session.json"


def get_hwid():

    raw = str(uuid.getnode())

    return hashlib.sha256(
        raw.encode()
    ).hexdigest()


def save_session(license_key):

    data = {
        "license_key": license_key
    }

    with open(SESSION_FILE, "w") as f:

        json.dump(data, f)


def load_session():

    if not os.path.exists(SESSION_FILE):
        return None

    with open(SESSION_FILE, "r") as f:

        return json.load(f)


def activate_license(license_key):

    payload = {
        "license_key": license_key,
        "hwid": get_hwid(),
        "device_name": os.environ.get(
            "COMPUTERNAME",
            "Windows PC"
        )
    }

    try:

        r = requests.post(
            f"{API_URL}/activate",
            json=payload
        )

        data = r.json()

        if data["success"]:

            save_session(license_key)

        return data

    except Exception as e:

        return {
            "success": False,
            "message": str(e)
        }


def verify_saved_license():

    session = load_session()

    if not session:

        return False

    payload = {
        "license_key": session["license_key"],
        "hwid": get_hwid()
    }

    try:

        r = requests.post(
            f"{API_URL}/verify",
            json=payload
        )

        data = r.json()

        return data["success"]

    except:

        return False