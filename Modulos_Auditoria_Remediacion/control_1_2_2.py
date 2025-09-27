import subprocess
import json

class control_1_2_2:
    def __init__(self):
        self.id = "1.2.2"
        self.title = "Ensure the latest software package is installed"
        self.description = "Verify that the latest version of NGINX is installed."

    def check(self):
        """Audit: check nginx package info"""
        try:
            result = subprocess.run(
                ["dnf", "info", "nginx"],
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE,
                universal_newlines=True
            )
            if result.returncode == 0 and "Version" in result.stdout:
                return {
                    "id": self.id,
                    "status": "PASS",
                    "output": result.stdout.strip()
                }
            else:
                return {
                    "id": self.id,
                    "status": "FAIL",
                    "output": "NGINX package info not found"
                }
        except FileNotFoundError:
            return {
                "id": self.id,
                "status": "ERROR",
                "output": "dnf command not found"
            }

    def remediate(self):
        """Remediation: update nginx package"""
        try:
            subprocess.run("dnf update -y nginx", shell=True, check=True)
            return {
                "id": self.id,
                "status": "REMEDIATED",
                "output": "NGINX package updated successfully"
            }
        except subprocess.CalledProcessError as e:
            return {
                "id": self.id,
                "status": "ERROR",
                "output": str(e)
            }

    def report(self):
        """Generate a JSON report"""
        result = self.check()
        return json.dumps(result, indent=4)


# Ejemplo de uso
if __name__ == "__main__":
    control = control_1_2_2()
    print("=== CHECK ===")
    print(control.report())

    if control.check()["status"] == "FAIL":
        print("=== REMEDIATING ===")
        print(control.remediate())
