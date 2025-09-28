import subprocess
import json
import re
import glob
import os

class control_2_4_2:
    def __init__(self):
        self.id = "2.4.2"
        self.title = "Ensure requests for unknown host names are rejected"
        self.description = "Verify that NGINX rejects requests with invalid Host headers."

    def check(self):
        """Audit: send curl request with invalid Host header"""
        try:
            result = subprocess.run(
                ["curl", "-k", "-o", "/dev/null", "-s", "-w", "%{http_code}", "https://127.0.0.1", "-H", "Host: invalid.host.com"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            status_code = result.stdout.strip()
        except FileNotFoundError:
            return {
                "id": self.id,
                "status": "ERROR",
                "output": "curl not found"
            }

        # Buscar si hay algún bloque server sin server_name
        files = ["/etc/nginx/nginx.conf"] + glob.glob("/etc/nginx/conf.d/*.conf")
        missing_server_names = []
        for f in files:
            if not os.path.exists(f):
                continue
            with open(f, "r") as conf:
                content = conf.read()
                blocks = re.findall(r"server\s*{.*?}", content, re.S)
                for block in blocks:
                    if "server_name" not in block:
                        missing_server_names.append(f)

        if status_code.startswith("4") and not missing_server_names:
            return {
                "id": self.id,
                "status": "PASS",
                "output": f"NGINX returned {status_code} for invalid host. All server blocks define server_name."
            }
        else:
            return {
                "id": self.id,
                "status": "FAIL",
                "output": f"NGINX returned {status_code} for invalid host OR missing server_name in: {missing_server_names}"
            }

    def remediate(self):
        """Remediation instructions (manual edit required)"""
        return {
            "id": self.id,
            "status": "MANUAL",
            "output": (
                "Add a default catch-all server block:\n"
                "server {\n"
                "    return 404;\n"
                "}\n\n"
                "Ensure every server block has an explicit server_name directive."
            )
        }

    def report(self):
        """Generate JSON report"""
        result = self.check()
        return json.dumps(result, indent=4)


# Ejemplo de uso
if __name__ == "__main__":
    control = control_2_4_2()
    print("=== CHECK ===")
    print(control.report())

    if control.check()["status"] == "FAIL":
        print("=== REMEDIATION REQUIRED ===")
        print(control.remediate())
