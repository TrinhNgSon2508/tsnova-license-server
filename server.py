from fastapi import FastAPI
from pydantic import BaseModel
from supabase import create_client
from datetime import datetime, timezone


app = FastAPI()

SUPABASE_URL = "https://kwrjbmxkgbdufdttmvqu.supabase.co"

SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imt3cmpibXhrZ2JkdWZkdHRtdnF1Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3ODQzMDM5OCwiZXhwIjoyMDk0MDA2Mzk4fQ.UWSh2UBNquy7aattJ63xhPEJgWdgBXwcBvct4_QbDeI"

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