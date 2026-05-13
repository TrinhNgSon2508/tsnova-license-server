from fastapi import FastAPI
from pydantic import BaseModel
from database import supabase
from datetime import datetime
import hashlib

app = FastAPI()


class ActivateRequest(BaseModel):
    license_key: str
    hwid: str
    device_name: str = "Unknown Device"


class VerifyRequest(BaseModel):
    license_key: str
    hwid: str


@app.get("/")
def home():
    return {"status": "TSNOVA API ONLINE"}


@app.get("/test-db")
def test_db():

    result = supabase.table("licenses") \
        .select("*") \
        .execute()

    return result.data


@app.post("/activate")
def activate(data: ActivateRequest):

    hwid_hash = hashlib.sha256(
        data.hwid.encode()
    ).hexdigest()

    # tìm license
    license_result = supabase.table("licenses") \
        .select("*") \
        .eq("license_key", data.license_key.strip()) \
        .execute()

    print(license_result.data)

    if not license_result.data:
        return {
            "success": False,
            "message": "Invalid license key"
        }

    license_data = license_result.data[0]

    # check status
    if license_data["status"] != "active":
        return {
            "success": False,
            "message": "License inactive"
        }

    # check expire
    expires_at = datetime.fromisoformat(
        license_data["expires_at"].replace("Z", "")
    )

    if expires_at < datetime.utcnow():
        return {
            "success": False,
            "message": "License expired"
        }

    # lấy plan
    plan_result = supabase.table("plans") \
        .select("*") \
        .eq("id", license_data["plan_id"]) \
        .execute()

    plan_data = plan_result.data[0]

    max_devices = plan_data["max_devices"]

    # check device tồn tại chưa
    existing_device = supabase.table("devices") \
        .select("*") \
        .eq("license_id", license_data["id"]) \
        .eq("hwid_hash", hwid_hash) \
        .execute()

    if existing_device.data:

        return {
            "success": True,
            "message": "Welcome back"
        }

    # đếm devices
    devices_result = supabase.table("devices") \
        .select("*") \
        .eq("license_id", license_data["id"]) \
        .execute()

    if len(devices_result.data) >= max_devices:

        return {
            "success": False,
            "message": "Device limit reached"
        }

    # add device
    supabase.table("devices").insert({
        "license_id": license_data["id"],
        "hwid_hash": hwid_hash,
        "device_name": data.device_name
    }).execute()

    return {
        "success": True,
        "message": "Activation successful"
    }


@app.post("/verify")
def verify(data: VerifyRequest):

    hwid_hash = hashlib.sha256(
        data.hwid.encode()
    ).hexdigest()

    # tìm license
    license_result = supabase.table("licenses") \
        .select("*") \
        .eq("license_key", data.license_key.strip()) \
        .execute()

    if not license_result.data:
        return {
            "success": False,
            "message": "Invalid license"
        }

    license_data = license_result.data[0]

    # check status
    if license_data["status"] != "active":
        return {
            "success": False,
            "message": "License inactive"
        }

    # check expire
    expires_at = datetime.fromisoformat(
        license_data["expires_at"].replace("Z", "")
    )

    if expires_at < datetime.utcnow():
        return {
            "success": False,
            "message": "License expired"
        }

    # check device
    device_result = supabase.table("devices") \
        .select("*") \
        .eq("license_id", license_data["id"]) \
        .eq("hwid_hash", hwid_hash) \
        .execute()

    if not device_result.data:
        return {
            "success": False,
            "message": "Device not activated"
        }

    # lấy plan
    plan_result = supabase.table("plans") \
        .select("*") \
        .eq("id", license_data["plan_id"]) \
        .execute()

    plan_name = "FREE"

    if plan_result.data:
        plan_name = plan_result.data[0]["name"]

    return {
        "success": True,
        "message": "License verified",
        "expires_at": license_data["expires_at"],
        "plan": plan_name
    }