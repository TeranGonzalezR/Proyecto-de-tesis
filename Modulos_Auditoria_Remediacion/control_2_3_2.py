import os
import stat
import subprocess
import json

class control_2_3_2:
    def __init__(self):
        self.id = "2.3.2"
        self.title = "Ensure access to NGINX directories and files is restricted"
        self.description = "Verify that NGINX directories and files in /etc/nginx follow least privilege principle."

    def check(self):
        """Audit: verify directory and file permissions"""
        base_path = "/etc/nginx"
        findings = []

        if not os.path.exists(base_path):
            return {
                "id": self.id,
                "status": "FAIL",
                "output": "/etc/nginx does not exist"
            }

        # Revisar directorios
        for root, dirs, files in os.walk(base_path):
            for d in dirs:
                dpath = os.path.join(root, d)
                mode = stat.S_IMODE(os.stat(dpath).st_mode)
                if mode > 0o755:
                    findings.append(f"Directory {dpath} has insecure permissions: {oct(mode)}")

            # Revisar archivos
            for f in files:
                fpath = os.path.join(root, f)
                mode = stat.S_IMODE(os.stat(fpath).st_mode)
                if mode > 0o660:
                    findings.append(f"File {fpath} has insecure permissions: {oct(mode)}")

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
                "output": "All NGINX directories and files comply with least privilege"
            }

    def remediate(self):
        """Remediation: fix permissions for directories and files"""
        try:
            subprocess.run("find /etc/nginx -type d -exec chmod go-w {} +", shell=True, check=True)
            subprocess.run("find /etc/nginx -type f -exec chmod ug-x,o-rwx {} +", shell=True, check=True)
            return {
                "id": self.id,
                "status": "REMEDIATED",
                "output": "Permissions for /etc/nginx directories and files adjusted"
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
    control = control_2_3_2()
    print("=== CHECK ===")
    print(control.report())

    if control.check()["status"] == "FAIL":
        print("=== REMEDIATING ===")
        print(control.remediate())
