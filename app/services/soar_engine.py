import subprocess
import shutil

class SOAREngine:
    def preflight_check(self):
        return True if shutil.which("ansible") else False

    def execute_action(self, action_category, target_ip=None):
        mapping = {"BLOCK_IP": "block_ip.yml", "ISOLATE_HOST": "isolate_host.yml"}
        playbook = mapping.get(action_category)
        
        if not playbook: return {"success": True, "output": "Notification Only"}
            
        cmd = ["ansible-playbook", f"playbooks/{playbook}", "--connection=local"]
        if target_ip: cmd.extend(["--extra-vars", f"target_ip={target_ip}"])
            
        try:
            res = subprocess.run(cmd, capture_output=True, text=True)
            return {"success": True, "output": res.stdout}
        except Exception as e:
            return {"success": False, "output": str(e)}