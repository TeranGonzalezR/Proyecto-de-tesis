import os
import pwd
import grp
import subprocess
import json

class control_2_3_1:
    def __init__(self):
        self.id = "2.3.1"
        self.title = "Ensure NGINX directories and files are owned by root"
        self.description = "Verify that /etc/nginx and its files are owned by root:root."

    def check(self):
        """Audit: verify ownership of /etc/nginx and its contents"""
        path = "/etc/nginx"
        findings = []

        if not os.path.exists(path):
            return {
                "id": self.id,
                "status": "FAIL",
                "output": "/etc/nginx does not exist"
            }

        for root, dirs, files in os.walk(path):
            for name in [*dirs, *files]:
                fpath = os.path.join(root, name)
                try:
                    st = os.stat(fpath)
                    owner = pwd.getpwuid(st.st_uid).pw_name
                    group = grp.getgrgid(st.st_gid).gr_name
                    if owner != "root" or group != "root":
                        findings.append(f"{fpath} owned by {owner}:{group}")
                except Exception as e:
                    findings.append(f"Error checking {fpath}: {e}")

        if findings:
            return {
                "id": self.id,
                "status": "FAIL",
                "output": "Non-root ownership found:\n" + "\n".join(findings)
            }
        else:
            return {
                "id": self.id,
                "status": "PASS",
                "output": "All files in /etc/nginx are owned by root:root"
            }

    def remediate(self):
        """Remediation: set ownership of /etc/nginx to root:root"""
        try:
            subprocess.run("chown -R root:root /etc/nginx", shell=True, check=True)
            return {
                "id": self.id,
                "status": "REMEDIATED",
                "output": "Ownership of /etc/nginx set to root:root"
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
    control = control_2_3_1()
    print("=== CHECK ===")
    print(control.report())

    if control.check()["status"] == "FAIL":
        print("=== REMEDIATING ===")
        print(control.remediate())
