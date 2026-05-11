from fastapi import FastAPI
from dotenv import load_dotenv
from supabase import create_client
from pydantic import BaseModel

import os

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

print("URL =", SUPABASE_URL)


supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)

app = FastAPI()


class ActivateRequest(BaseModel):
    license_key: str
    hwid: str


@app.get("/")
def home():
    return {"status": "online"}


@app.post("/activate")
def activate(data: ActivateRequest):

    # tìm license
    result = supabase.table("licenses1") \
        .select("*") \
        .eq("license_key", data.license_key.strip()) \
        .execute()
    print("KEY =", data.license_key)
    print("TABLE = licenses1")
    print("RESULT =", result.data)

    if not result.data:
        return {
            "success": False,
            "message": "Invalid license key"
        }

    license_data = result.data[0]

    if not license_data["active"]:
        return {
            "success": False,
            "message": "License disabled"
        }

    license_id = license_data["id"]
    max_devices = license_data["max_devices"]

    # lấy devices hiện tại
    devices = supabase.table("device_bindings") \
        .select("*") \
        .eq("license_id", license_id) \
        .execute()

    device_list = devices.data

    # check HWID đã tồn tại chưa
    for device in device_list:

        if device["hwid"] == data.hwid:

            return {
                "success": True,
                "message": "Welcome back"
            }

    # vượt quá số máy
    if len(device_list) >= max_devices:

        return {
            "success": False,
            "message": "Device limit reached"
        }

    # thêm máy mới
    supabase.table("device_bindings") \
        .insert({
            "license_id": license_id,
            "hwid": data.hwid
        }) \
        .execute()

    return {
        "success": True,
        "message": "New device activated"
    }