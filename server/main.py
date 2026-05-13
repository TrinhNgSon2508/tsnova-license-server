from fastapi import FastAPI
from pydantic import BaseModel
from database import supabase
from datetime import datetime
import hashlib
import secrets
from datetime import timedelta

app = FastAPI()


# =========================
# MODELS
# =========================

class ActivateRequest(BaseModel):
    license_key: str
    hwid: str
    device_name: str = "Unknown Device"


class VerifyRequest(BaseModel):
    license_key: str
    hwid: str

class CreateLicenseRequest(BaseModel):
    plan_id: str
    days: int = 30


# =========================
# HOME
# =========================

@app.get("/")
def home():
    return {"status": "TSNOVA API ONLINE"}


# =========================
# ACTIVATE
# =========================

@app.post("/activate")
def activate(data: ActivateRequest):

    # hash HWID
    hwid_hash = hashlib.sha256(data.hwid.encode()).hexdigest()

    # tìm license
    license_result = supabase.table("licenses") \
        .select("*") \
        .eq("license_key", data.license_key) \
        .execute()

    if not license_result.data:
        return {"success": False, "message": "Invalid license"}

    license_data = license_result.data[0]

    # check status
    if license_data["status"] != "active":
        return {"success": False, "message": "License not active"}

    # check expire
    expires_at = datetime.fromisoformat(
        license_data["expires_at"].replace("Z", "")
    )

    if expires_at < datetime.utcnow():
        return {"success": False, "message": "License expired"}

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

        # update last_seen
        supabase.table("devices") \
            .update({
                "last_seen": datetime.utcnow().isoformat()
            }) \
            .eq("id", existing_device.data[0]["id"]) \
            .execute()

        return {
            "success": True,
            "message": "Device already activated"
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
        "device_name": data.device_name,
        "last_seen": datetime.utcnow().isoformat()
    }).execute()

    return {
        "success": True,
        "message": "Activation successful"
    }


# =========================
# VERIFY
# =========================

@app.post("/verify")
def verify(data: VerifyRequest):

    hwid_hash = hashlib.sha256(data.hwid.encode()).hexdigest()

    # tìm license
    license_result = supabase.table("licenses") \
        .select("*") \
        .eq("license_key", data.license_key) \
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

    # update last_seen
    supabase.table("devices") \
        .update({
            "last_seen": datetime.utcnow().isoformat()
        }) \
        .eq("id", device_result.data[0]["id"]) \
        .execute()

    plan_result = supabase.table("plans") \
        .select("*") \
        .eq("id", license_data["plan_id"]) \
        .execute()

    plan_data = plan_result.data[0]

    return {
        "success": True,
        "message": "License verified",
        "expires_at": license_data["expires_at"],
        "plan": plan_data["name"]
    }
@app.post("/create-license")
def create_license(data: CreateLicenseRequest):

    # check plan
    plan_result = supabase.table("plans") \
        .select("*") \
        .eq("id", data.plan_id) \
        .execute()

    if not plan_result.data:
        return {
            "success": False,
            "message": "Invalid plan"
        }

    # generate key
    random_part = secrets.token_hex(4).upper()

    license_key = f"TSNOVA-{random_part}"

    # expire
    expires_at = (
        datetime.utcnow() +
        timedelta(days=data.days)
    ).isoformat()

    # insert
    supabase.table("licenses").insert({
        "license_key": license_key,
        "plan_id": data.plan_id,
        "status": "active",
        "expires_at": expires_at
    }).execute()

    return {
        "success": True,
        "license_key": license_key,
        "expires_at": expires_at
    }