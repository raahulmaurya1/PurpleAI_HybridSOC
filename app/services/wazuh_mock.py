import random
import time
from datetime import datetime

class WazuhMock:
    def __init__(self):
        self.attack_library = {
            "sqli": {"name": "SQL Injection", "rule_id": 31101, "level": 12, "desc": "SQL Injection in URI", "payloads": ["' OR 1=1 --", "UNION SELECT user,pass"]},
            "ransomware": {"name": "Ransomware", "rule_id": 1005, "level": 14, "desc": "Mass file encryption detected", "payloads": ["/home/user/*.enc"]},
            "ddos": {"name": "DDoS Attack", "rule_id": 31509, "level": 13, "desc": "High connection rate", "payloads": ["Rate: 9000/s"]},
            "brute_force": {"name": "SSH Brute Force", "rule_id": 5712, "level": 10, "desc": "Failed SSH logins", "payloads": ["User: root"]},
            "xss": {"name": "XSS Attack", "rule_id": 31103, "level": 10, "desc": "Script tag in URI", "payloads": ["<script>alert(1)</script>"]},
            "mitm": {"name": "ARP Spoofing", "rule_id": 8001, "level": 12, "desc": "Duplicate MAC detected", "payloads": ["ARP Conflict"]},
            "c2_beacon": {"name": "C2 Traffic", "rule_id": 1006, "level": 14, "desc": "Botnet Communication", "payloads": ["Dest: Malicious_IP"]},
            "priv_esc": {"name": "Privilege Esc", "rule_id": 553, "level": 13, "desc": "Sudoers modified", "payloads": ["/etc/sudoers"]},
            "fim": {"name": "FIM Alert", "rule_id": 550, "level": 7, "desc": "Critical file changed", "payloads": ["/etc/passwd"]},
            "data_exfil": {"name": "Data Exfiltration", "rule_id": 1007, "level": 13, "desc": "Large upload detected", "payloads": ["Upload: 5GB"]}
        }

    def _generate_ip(self):
        return f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"

    def generate_noise(self):
        return [{
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "rule_id": 1001, "level": 3, "description": "System Idle / Background Noise",
            "src_ip": self._generate_ip(), "details": "Normal Activity"
        }]

    def fetch_logs(self, attack_key):
        time.sleep(1)
        if attack_key == "random_unknown":
            return [{
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "rule_id": 99999, "level": random.randint(10, 15),
                "description": "Anomalous Heuristic Detection",
                "src_ip": self._generate_ip(), "details": "Unknown Pattern"
            }]
            
        template = self.attack_library.get(attack_key, self.attack_library["brute_force"])
        return [{
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "rule_id": template["rule_id"], "level": template["level"],
            "description": template["description"], "src_ip": self._generate_ip(),
            "details": random.choice(template["payloads"])
        }]