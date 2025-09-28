import os
import stat
import pwd
import grp
import subprocess
import json

class control_2_3_3:
    def __init__(self):
        self.id = "2.3.3"
        self.title = "Ensure the NGINX process ID (PID) file is secured"
        self.description = "Verify that /var/run/nginx.pid is owned by root:root and has permissions 644."

    def check(self):
        """Audit: verify ownership and permissions of nginx.pid"""
        pid_file = "/var/run/nginx.pid"

        if not os.path.exists(pid_file):
            return {
                "id": self.id,
                "status": "FAIL",
                "output": f"{pid_file} does not exist"
            }

        try:
            st = os.stat(pid_file)
            owner = pwd.getpwuid(st.st_uid).pw_name
            group = grp.getgrgid(st.st_gid).gr_name
            mode = stat.S_IMODE(st.st_mode)

            findings = []
            if owner != "root" or group != "root":
                findings.append(f"Owner/Group is {owner}:{group}, expected root:root")
            if mode != 0o644:
                findings.append(f"Permissions are {oct(mode)}, expected 0o644")

            if findings:
                return {
                    "id": self.id,
                    "status": "FAIL",
                    "output": "\n".join(findings)
                }
            else:
                return {
                    "id": self.id,
                    "status": "PASS",
                    "output": f"{pid_file} is properly secured (owner root:root, perms 644)"
                }

        except Exception as e:
            return {
                "id": self.id,
                "status": "ERROR",
                "output": str(e)
            }

    def remediate(self):
        """Remediation: set correct owner and permissions for nginx.pid"""
        pid_file = "/var/run/nginx.pid"
        if not os.path.exists(pid_file):
            return {
                "id": self.id,
                "status": "ERROR",
                "output": f"{pid_file} not found"
            }
        try:
            subprocess.run(f"chown root:root {pid_file}", shell=True, check=True)
            subprocess.run(f"chmod 644 {pid_file}", shell=True, check=True)
            return {
                "id": self.id,
                "status": "REMEDIATED",
                "output": f"{pid_file} ownership set to root:root and permissions set to 644"
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
    control = control_2_3_3()
    print("=== CHECK ===")
    print(control.report())

    if control.check()["status"] == "FAIL":
        print("=== REMEDIATING ===")
        print(control.remediate())
