import sqlite3
import json
from datetime import datetime

DB_NAME = "purple_ai.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS incidents
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  timestamp TEXT, attack_type TEXT, src_ip TEXT, status TEXT, 
                  severity INTEGER, logs TEXT, ai_analysis TEXT, remediation_log TEXT)''')
    conn.commit()
    conn.close()

def create_incident(attack_type, src_ip, logs):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO incidents (timestamp, attack_type, src_ip, status, logs) VALUES (?, ?, ?, ?, ?)",
              (timestamp, attack_type, src_ip, "Analyzing", json.dumps(logs)))
    incident_id = c.lastrowid
    conn.commit()
    conn.close()
    return incident_id

def count_past_incidents(src_ip):
    if not src_ip: return 0
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM incidents WHERE src_ip=?", (src_ip,))
    count = c.fetchone()[0]
    conn.close()
    return count

def update_incident_analysis(incident_id, severity, ai_analysis, status):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE incidents SET severity=?, ai_analysis=?, status=? WHERE id=?",
              (severity, ai_analysis, status, incident_id))
    conn.commit()
    conn.close()

def resolve_incident(incident_id, remediation_log):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE incidents SET status=?, remediation_log=? WHERE id=?",
              ("Resolved", remediation_log, incident_id))
    conn.commit()
    conn.close()

def get_incident(incident_id):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM incidents WHERE id=?", (incident_id,))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None