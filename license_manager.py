import json
import os

from activate_client import activate_license


LICENSE_FILE = "license.json"


def save_license_key(key):

    with open(LICENSE_FILE, "w") as f:

        json.dump({
            "license_key": key
        }, f)


def load_license_key():

    if not os.path.exists(LICENSE_FILE):
        return None

    try:

        with open(LICENSE_FILE, "r") as f:

            data = json.load(f)

            return data.get("license_key")

    except:
        return None


def verify_saved_license():

    key = load_license_key()

    if not key:
        return False

    result = activate_license(key)

    return result.get("success", False)