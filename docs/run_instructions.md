# Run instructions & how to enable GitHub Pages

1. Enable GitHub Pages
   - Go to Settings → Pages in this repository
   - Source: Branch = <strong>main</strong>, Folder = <strong>/docs</strong>
   - Save. The site will be available at: https://<your-username>.github.io/CRM/ (may take a minute)

2. Run VisaAgent prototype locally
   - cd docs/visa_agent_prototype
   - python -m venv venv
   - source venv/bin/activate
   - pip install -r requirements.txt
   - uvicorn visa_agent_main:app --reload --port 8000

3. Generate agencies CSV (staging)
   - cd docs/agencies
   - pip install faker
   - python generate_agencies.py
   - Import agencies_kerala_tn.csv into Postgres using \copy or psql

4. Helpful URLs
   - OpenAPI spec: /docs/openapi_v1.yaml
   - VisaAgent prototype endpoints (after running):
     - POST /api/v1/agencies/register
     - POST /api/v1/visas/requests
     - POST /api/v1/agencies/{agency_id}/respond_lead

