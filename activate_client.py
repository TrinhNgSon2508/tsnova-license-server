import requests

from hwid import get_hwid
import time


API_URL = "https://tsnova-license-server-1.onrender.com/activate"


def activate_license(license_key):
    hwid = get_hwid()
    payload = {"license_key": license_key, "hwid": hwid}

    for _ in range(3):  # thử 3 lần
        try:
            response = requests.post(API_URL, json=payload, timeout=60)
            return response.json()
        except Exception as e:
            time.sleep(5)  # chờ 5 giây rồi retry
            last_error = str(e)

    return {"success": False, "message": last_error}