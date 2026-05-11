from fastapi import FastAPI
from pydantic import BaseModel
from supabase import create_client
from datetime import datetime, timezone
import os


app = FastAPI()

SUPABASE_URL = os.getenv("SUPABASE_URL")

SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)

MAX_DEVICES = 2


class VerifyRequest(BaseModel):
    license_key: str
    hwid: str


@app.post("/verify")
def verify(data: VerifyRequest):

    result = supabase.table("licenses") \
        .select("*") \
        .eq("license_key", data.license_key) \
        .execute()

    if not result.data:
        return {
            "valid": False,
            "reason": "key not found"
        }

    row = result.data[0]

    # expire check
    expire = datetime.fromisoformat(
        row["expire_date"]
    )

    

    if expire.replace(tzinfo=None) < datetime.utcnow():

        return {
            "valid": False,
            "reason": "expired"
        }

    hwid = row.get("hwid") or []

    # máy đã tồn tại
    if data.hwid in hwid:

        return {
            "valid": True,
            "plan": row["plan"]
        }

    # quá số máy
    if len(hwid) >= MAX_DEVICES:

        return {
            "valid": False,
            "reason": "device limit reached"
        }

    # add machine
    hwid.append(data.hwid)

    supabase.table("licenses") \
        .update({
            "hwid": hwid
        }) \
        .eq("license_key", data.license_key) \
        .execute()

    return {
        "valid": True,
        "plan": row["plan"],
        "expire_date": row["expire_date"]
    }