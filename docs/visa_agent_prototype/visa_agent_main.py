from fastapi import FastAPI, UploadFile, File, Form, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional
import uuid, os, json, asyncio, random

app = FastAPI(title="VisaAgent Prototype")

# In-memory stores for prototype (replace with DB in production)
AGENCIES = {}
VISA_REQUESTS = {}
CHAT_SESSIONS = {}

# Simple scoring rules example
def score_agency(agency, country):
    score = 0
    if country in agency.get("specialization_countries", []):
        score += 50
    score += agency.get("success_rate", 80) / 2  # up to 50
    if agency.get("status") == "active":
        score += 10
    score += max(0, 10 - agency.get("avg_response_time", 5))
    return score

@app.post("/api/v1/ai/ocr/extract")
async def ocr_extract(file: UploadFile = File(...)):
    file_id = str(uuid.uuid4())
    saved = f"/tmp/{file_id}_{file.filename}"
    with open(saved, "wb") as f:
        f.write(await file.read())
    ocr_result = {
        "file_id": file_id,
        "filename": file.filename,
        "text": "Simulated OCR text",
        "passport_number": "N0123456",
        "name": "Test User",
        "expiry": "2030-01-01",
        "confidence": 0.95
    }
    return {"ocr": ocr_result}

class VisaCreate(BaseModel):
    user_id: str
    country: str
    visa_type: str
    travel_from: Optional[str] = None
    travel_to: Optional[str] = None
    max_agencies_to_ping: Optional[int] = 10

@app.post("/api/v1/visas/requests")
async def create_visa_request(payload: VisaCreate, background_tasks: BackgroundTasks):
    req_id = str(uuid.uuid4())
    VISA_REQUESTS[req_id] = {
        "id": req_id,
        "user_id": payload.user_id,
        "country": payload.country,
        "visa_type": payload.visa_type,
        "status": "new",
        "documents": [],
        "pinged_agencies": []
    }
    background_tasks.add_task(match_and_ping_agencies, req_id, payload.max_agencies_to_ping)
    return {"request_id": req_id, "status": "queued"}

async def match_and_ping_agencies(request_id: str, k: int):
    req = VISA_REQUESTS[request_id]
    country = req["country"]
    ranked = []
    for aid, a in AGENCIES.items():
        sc = score_agency(a, country)
        ranked.append((sc, aid))
    ranked.sort(reverse=True)
    selected = [aid for _, aid in ranked[:k]]
    req["pinged_agencies"] = selected
    req["status"] = "pinged"
    for aid in selected:
        AGENCIES[aid].setdefault("inbox", []).append({"lead_id": request_id, "country": country})
    await asyncio.sleep(30)
    if req.get("assigned_agency"):
        req["status"] = "assigned"
    else:
        if selected:
            req["assigned_agency"] = selected[0]
            req["status"] = "assigned"
            csid = str(uuid.uuid4())
            CHAT_SESSIONS[csid] = {"id": csid, "user_id": req["user_id"], "agency_id": selected[0], "messages": []}
            req["chat_session_id"] = csid

@app.post("/api/v1/agencies/register")
async def register_agency(name: str = Form(...), state: str = Form(...), city: str = Form(...)):
    aid = str(uuid.uuid4())
    AGENCIES[aid] = {
        "id": aid,
        "name": name,
        "state": state,
        "city": city,
        "specialization_countries": ["UAE","Schengen"] if random.choice([True, False]) else ["Thailand","Malaysia"],
        "success_rate": 90.0,
        "status": "active",
        "avg_response_time": 5
    }
    return {"agency_id": aid}

@app.post("/api/v1/agencies/{agency_id}/respond_lead")
async def agency_respond(agency_id: str, lead_id: str = Form(...), action: str = Form(...)):
    if agency_id not in AGENCIES:
        raise HTTPException(status_code=404, detail="agency not found")
    req = VISA_REQUESTS.get(lead_id)
    if not req:
        raise HTTPException(status_code=404, detail="lead not found")
    AGENCIES[agency_id].setdefault("responses", []).append({"lead_id": lead_id, "action": action})
    if action == "accept":
        req["assigned_agency"] = agency_id
        req["status"] = "assigned"
        csid = str(uuid.uuid4())
        CHAT_SESSIONS[csid] = {"id": csid, "user_id": req["user_id"], "agency_id": agency_id, "messages": []}
        req["chat_session_id"] = csid
        return {"status": "assigned", "chat_session_id": csid}
    return {"status": "rejected"}

@app.get("/api/v1/visas/requests/{id}")
async def get_visa_request(id: str):
    req = VISA_REQUESTS.get(id)
    if not req:
        raise HTTPException(status_code=404)
    return req

@app.get("/api/v1/chat/sessions/{id}")
async def get_chat_session(id: str):
    cs = CHAT_SESSIONS.get(id)
    if not cs:
        raise HTTPException(status_code=404)
    return cs
