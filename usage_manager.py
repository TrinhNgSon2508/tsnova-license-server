import os
import json
from datetime import datetime

USAGE_FILE = "usage.json"

FREE_LIMIT = 10


def load_usage():

    today = datetime.now().strftime("%Y-%m-%d")

    if not os.path.exists(USAGE_FILE):

        data = {
            "date": today,
            "used": 0,
            "plan": "free"
        }

        save_usage(data)

        return data

    with open(USAGE_FILE, "r") as f:
        data = json.load(f)

    # reset mỗi ngày
    if data["date"] != today:

        data["date"] = today
        data["used"] = 0

        save_usage(data)

    return data


def save_usage(data):

    with open(USAGE_FILE, "w") as f:
        json.dump(data, f, indent=4)


def can_use():

    data = load_usage()

    if data["plan"] != "free":
        return True

    return data["used"] < FREE_LIMIT


def add_usage():

    data = load_usage()

    data["used"] += 1

    save_usage(data)


def get_remaining():

    data = load_usage()

    if data["plan"] != "free":
        return "Unlimited"

    return FREE_LIMIT - data["used"]


def get_plan():

    data = load_usage()

    return data["plan"]