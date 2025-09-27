import subprocess
import json
import pwd

class control_2_2_2:
    def __init__(self):
        self.id = "2.2.2"
        self.title = "Ensure the NGINX service account is locked"
        self.description = "Verify that the nginx service account is locked to prevent direct logins."

    def get_nginx_user(self):
        """Leer el usuario definido en nginx.conf"""
        try:
            with open("/etc/nginx/nginx.conf", "r") as conf:
                for line in conf:
                    if line.strip().startswith("user"):
                        parts = line.strip().split()
                        if len(parts) >= 2:
                            return parts[1].replace(";", "")
        except FileNotFoundError:
            return None
        return None

    def check(self):
        """Audit: verify that the nginx user account is locked"""
        nginx_user = self.get_nginx_user()
        if not nginx_user:
            return {
                "id": self.id,
                "status": "FAIL",
                "output": "No user directive found in /etc/nginx/nginx.conf"
            }

        try:
            result = subprocess.run(
                ["passwd", "-S", nginx_user],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            if result.returncode == 0:
                if "LK" in result.stdout:
                    return {
                        "id": self.id,
                        "status": "PASS",
                        "output": result.stdout.strip()
                    }
                else:
                    return {
                        "id": self.id,
                        "status": "FAIL",
                        "output": f"User {nginx_user} is not locked:\n{result.stdout.strip()}"
                    }
            else:
                return {
                    "id": self.id,
                    "status": "ERROR",
                    "output": result.stderr.strip()
                }
        except FileNotFoundError:
            return {
                "id": self.id,
                "status": "ERROR",
                "output": "passwd command not found"
            }

    def remediate(self):
        """Remediation: lock nginx service account"""
        nginx_user = self.get_nginx_user()
        if not nginx_user:
            return {
                "id": self.id,
                "status": "ERROR",
                "output": "No nginx user found to lock"
            }
        try:
            subprocess.run(f"passwd -l {nginx_user}", shell=True, check=True)
            return {
                "id": self.id,
                "status": "REMEDIATED",
                "output": f"User {nginx_user} has been locked"
            }
        except subprocess.CalledProcessError as e:
            return {
                "id": self.id,
                "status": "ERROR",
                "output": str(e)
            }

    def report(self):
        """Generate JSON report"""
        result = self.check()
        return json.dumps(result, indent=4)


# Ejemplo de uso
if __name__ == "__main__":
    control = control_2_2_2()
    print("=== CHECK ===")
    print(control.report())

    if control.check()["status"] == "FAIL":
        print("=== REMEDIATING ===")
        print(control.remediate())
