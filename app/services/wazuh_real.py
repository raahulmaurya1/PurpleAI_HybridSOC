import requests
import urllib3
import base64
import os
from dotenv import load_dotenv

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
load_dotenv()

class WazuhReal:
    def __init__(self):
        self.url = os.getenv("WAZUH_URL")
        self.user = os.getenv("WAZUH_USER")
        self.password = os.getenv("WAZUH_PASS")
        self.token = None

    def _authenticate(self):
        if not self.url: return False
        login_url = f"{self.url}/security/user/authenticate"
        basic_auth = f"{self.user}:{self.password}".encode('utf-8')
        headers = {'Authorization': f'Basic {base64.b64encode(basic_auth).decode("utf-8")}'}
        try:
            res = requests.get(login_url, headers=headers, verify=False, timeout=2)
            if res.status_code == 200:
                self.token = res.json()['data']['token']
                return True
        except: pass
        return False

    def fetch_latest_logs(self):
        if not self.token and not self._authenticate(): return None
        api_url = f"{self.url}/security/alerts?limit=5&sort=-timestamp"
        headers = {'Authorization': f'Bearer {self.token}'}
        try:
            res = requests.get(api_url, headers=headers, verify=False, timeout=3)
            if res.status_code == 200:
                data = res.json()
                logs = []
                for item in data['data']['items']:
                    logs.append({
                        "timestamp": item['timestamp'],
                        "rule_id": item['rule']['id'],
                        "level": item['rule']['level'],
                        "description": item['rule']['description'],
                        "src_ip": item['data'].get('src_ip', 'Internal'),
                        "details": item.get('full_log', 'Real Event')
                    })
                return logs
        except: pass
        return None