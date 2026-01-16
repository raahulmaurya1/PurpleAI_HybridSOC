import secrets
import os
from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, Response
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from dotenv import load_dotenv
from app.services import db_manager, wazuh_mock, wazuh_real, ai_analyst, soar_engine, reporter, threat_intel

load_dotenv()
app = FastAPI(title="PurpleAI Hybrid SOC")
security = HTTPBasic()
templates = Jinja2Templates(directory="templates")

# Initialize Services
mock_client = wazuh_mock.WazuhMock()
real_client = wazuh_real.WazuhReal()
ai = ai_analyst.AIAnalyst()
soar = soar_engine.SOAREngine()
intel = threat_intel.ThreatIntel()
pdf_reporter = reporter.IncidentReporter()

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    user = os.getenv("ADMIN_USER", "admin")
    pwd = os.getenv("ADMIN_PASS", "purpleai123")
    if not (secrets.compare_digest(credentials.username, user) and 
            secrets.compare_digest(credentials.password, pwd)):
        raise HTTPException(status_code=401, detail="Unauthorized", headers={"WWW-Authenticate": "Basic"})
    return credentials.username

@app.on_event("startup")
def startup():
    db_manager.init_db()
    soar.preflight_check()

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request, username: str = Depends(get_current_username)):
    return templates.TemplateResponse("index.html", {"request": request, "user": username, "attacks": mock_client.attack_library})

@app.get("/live_feed")
async def live_feed(username: str = Depends(get_current_username)):
    """Attempts Real API first, falls back to Mock Noise"""
    use_real = os.getenv("USE_REAL_MONITOR", "False").lower() == "true"
    if use_real:
        real_logs = real_client.fetch_latest_logs()
        if real_logs: return real_logs
    return mock_client.generate_noise()

@app.post("/simulate_attack")
async def simulate_attack(payload: dict, username: str = Depends(get_current_username)):
    """Simulations ALWAYS use Mock Client"""
    requested_type = payload.get("attack_type")
    logs = mock_client.fetch_logs(requested_type)
    src_ip = logs[0].get("src_ip")
    
    incident_id = db_manager.create_incident(requested_type, src_ip, logs)
    history = db_manager.count_past_incidents(src_ip)
    score = intel.check_ip_reputation(src_ip)
    
    analysis = ai.analyze_universal(logs, score, history)
    severity = analysis.get("severity", 0)
    action = analysis.get("recommended_action")
    status = "Pending Approval"
    
    if severity >= 12 and action != "NOTIFY_ONLY":
        soar_res = soar.execute_action(action, target_ip=src_ip)
        status = "Resolved (Auto)" if soar_res['success'] else "Auto-Fix Failed"
        db_manager.resolve_incident(incident_id, soar_res['output'])
    elif action == "NOTIFY_ONLY":
        status = "Logged"
        db_manager.resolve_incident(incident_id, "Notification Only")

    db_manager.update_incident_analysis(incident_id, severity, analysis['explanation'], status)
    
    return {
        "incident_id": incident_id, "logs": logs, "ai_analysis": analysis,
        "status": status, "intel": {"history": history, "score": score},
        "target_ip": src_ip
    }

@app.post("/approve_remediation/{incident_id}")
async def approve(incident_id: int, payload: dict, username: str = Depends(get_current_username)):
    res = soar.execute_action(payload.get("action"), target_ip=payload.get("target_ip"))
    db_manager.resolve_incident(incident_id, res['output'])
    return {"status": "Resolved", "output": res['output']}

@app.get("/download_report/{incident_id}")
async def download_report(incident_id: int, username: str = Depends(get_current_username)):
    incident = db_manager.get_incident(incident_id)
    if not incident: raise HTTPException(status_code=404)
    pdf_bytes = pdf_reporter.generate(incident)
    return Response(content=pdf_bytes, media_type="application/pdf", headers={"Content-Disposition": f"attachment; filename=report_{incident_id}.pdf"})