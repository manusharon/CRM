# VisaAgent Prototype (FastAPI)

This folder contains a small prototype of the VisaAgent microservice. It is intentionally simple and uses in-memory stores; replace with Postgres/Redis and queue for production.

Files:
- visa_agent_main.py : FastAPI app
- requirements.txt
- Dockerfile

Run locally:
1. python -m venv venv && source venv/bin/activate
2. pip install -r requirements.txt
3. uvicorn visa_agent_main:app --reload --port 8000

Endpoints:
- POST /api/v1/agencies/register -> register a demo agency
- POST /api/v1/visas/requests -> create visa request (background match & ping)
- POST /api/v1/agencies/{agency_id}/respond_lead -> agency accepts/rejects
- GET /api/v1/visas/requests/{id} -> view request
- GET /api/v1/chat/sessions/{id} -> view chat session
