import requests

from hwid import get_hwid


API_URL = "https://tsnova-api.onrender.com/activate"


def activate_license(license_key):

    hwid = get_hwid()

    payload = {
        "license_key": license_key,
        "hwid": hwid
    }

    try:

        response = requests.post(
            API_URL,
            json=payload
        )

        return response.json()

    except Exception as e:

        return {
            "success": False,
            "message": str(e)
        }