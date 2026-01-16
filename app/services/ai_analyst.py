import google.generativeai as genai
import json
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class AIAnalyst:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def analyze_universal(self, logs, threat_score, history_count):
        prompt = f"""
        Act as a Tier 3 SOC Analyst. Analyze these logs: {logs}
        Context: Threat Score: {threat_score}/100 | Past Offenses: {history_count}
        
        Task:
        1. Identify Attack Type.
        2. Assign Severity (1-15).
        3. Recommend Action: "BLOCK_IP", "ISOLATE_HOST", or "NOTIFY_ONLY".
        
        Return JSON ONLY:
        {{ "attack_type": "string", "explanation": "string", "severity": int, "recommended_action": "string" }}
        """
        try:
            response = self.model.generate_content(prompt)
            return json.loads(response.text.replace('```json', '').replace('```', '').strip())
        except:
            return {"attack_type": "Error", "explanation": "AI Failed", "severity": 0, "recommended_action": "NOTIFY_ONLY"}