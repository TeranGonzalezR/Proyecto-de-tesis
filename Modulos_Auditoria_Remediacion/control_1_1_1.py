import subprocess
import json

class control_1_1_1:
    def __init__(self):
        self.id = "1.1.1"
        self.title = "Ensure NGINX is installed"
        self.description = "Verify that NGINX is installed on the system."

    def check(self):
        """Audit: check if nginx is installed by running 'nginx -v'"""
        try:
            result = subprocess.run(
                ["nginx", "-v"],
                stderr=subprocess.PIPE,  # nginx -v prints to stderr
                stdout=subprocess.PIPE,
                text=True
            )
            if result.returncode == 0 and "nginx" in result.stderr.lower():
                return {"id": self.id, "status": "PASS", "output": result.stderr.strip()}
            else:
                return {"id": self.id, "status": "FAIL", "output": "Nginx not detected"}
        except FileNotFoundError:
            return {"id": self.id, "status": "FAIL", "output": "Nginx command not found"}

    def remediate(self):
        """Apply remediation: install nginx (example with dnf for RHEL/Fedora)"""
        try:
            commands = [
                "dnf update -y && dnf install -y dnf-utils",
                """cat << EOF > /etc/yum.repos.d/nginx.repo
[nginx-stable]
name=nginx stable repo
baseurl=https://nginx.org/packages/rhel/9/x86_64/
gpgcheck=1
enabled=1
gpgkey=https://nginx.org/keys/nginx_signing.key
module_hotfixes=true
EOF""",
                "dnf install -y nginx"
            ]
            for cmd in commands:
                subprocess.run(cmd, shell=True, check=True)
            return {"id": self.id, "status": "REMEDIATED", "output": "Nginx installed successfully"}
        except subprocess.CalledProcessError as e:
            return {"id": self.id, "status": "ERROR", "output": str(e)}

    def report(self):
        """Generate a JSON report"""
        result = self.check()
        return json.dumps(result, indent=4)
    
    # Ejemplo de uso
if __name__ == "__main__":
    control = control_1_1_1()
    print("=== CHECK ===")
    print(control.report())

    if control.check()["status"] == "FAIL":
        print("=== REMEDIATING ===")
        print(control.remediate())
