import random
class ThreatIntel:
    def check_ip_reputation(self, ip):
        if not ip: return 0
        return random.randint(10, 95)