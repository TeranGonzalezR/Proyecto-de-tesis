import subprocess
import json
import pwd

class control_2_2_3:
    def __init__(self):
        self.id = "2.2.3"
        self.title = "Ensure the NGINX service account has an invalid shell"
        self.description = "Verify that the nginx service account cannot log in by ensuring its shell is /sbin/nologin."

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
        """Audit: verify that the nginx user has /sbin/nologin as shell"""
        nginx_user = self.get_nginx_user()
        if not nginx_user:
            return {
                "id": self.id,
                "status": "FAIL",
                "output": "No user directive found in /etc/nginx/nginx.conf"
            }

        try:
            user_info = pwd.getpwnam(nginx_user)
            shell = user_info.pw_shell
            if "nologin" in shell:
                return {
                    "id": self.id,
                    "status": "PASS",
                    "output": f"User {nginx_user} has invalid shell: {shell}"
                }
            else:
                return {
                    "id": self.id,
                    "status": "FAIL",
                    "output": f"User {nginx_user} has a valid shell: {shell}"
                }
        except KeyError:
            return {
                "id": self.id,
                "status": "FAIL",
                "output": f"User {nginx_user} not found in system"
            }

    def remediate(self):
        """Remediation: change nginx user shell to /sbin/nologin"""
        nginx_user = self.get_nginx_user()
        if not nginx_user:
            return {
                "id": self.id,
                "status": "ERROR",
                "output": "No nginx user found to remediate"
            }
        try:
            subprocess.run(f"usermod -s /sbin/nologin {nginx_user}", shell=True, check=True)
            return {
                "id": self.id,
                "status": "REMEDIATED",
                "output": f"User {nginx_user} shell set to /sbin/nologin"
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
    control = control_2_2_3()
    print("=== CHECK ===")
    print(control.report())

    if control.check()["status"] == "FAIL":
        print("=== REMEDIATING ===")
        print(control.remediate())
