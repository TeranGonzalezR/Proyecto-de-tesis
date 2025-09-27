import subprocess
import json

class control_1_2_1:
    def __init__(self):
        self.id = "1.2.1"
        self.title = "Ensure package manager repositories are properly configured"
        self.description = "Verify that package manager repositories are correctly configured to receive security updates."

    def check(self):
        """Audit: check if nginx-stable repo is present"""
        try:
            result = subprocess.run(
                ["dnf", "repolist", "-v", "nginx-stable"],
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE,
                universal_newlines=True
            )
            if result.returncode == 0 and "nginx-stable" in result.stdout:
                return {"id": self.id, "status": "PASS", "output": "nginx-stable repo is configured"}
            else:
                return {"id": self.id, "status": "FAIL", "output": "nginx-stable repo not found"}
        except FileNotFoundError:
            return {"id": self.id, "status": "ERROR", "output": "dnf command not found"}

    def remediate(self):
        """Remediation: configure nginx.org stable repository"""
        try:
            repo_config = """cat << EOF > /etc/yum.repos.d/nginx.repo
[nginx-stable]
name=nginx stable repo
baseurl=http://nginx.org/packages/rhel/8/$basearch/
gpgcheck=1
enabled=1
gpgkey=https://nginx.org/keys/nginx_signing.key
module_hotfixes=true
EOF"""
            subprocess.run(repo_config, shell=True, check=True)
            return {"id": self.id, "status": "REMEDIATED", "output": "nginx-stable repo configured"}
        except subprocess.CalledProcessError as e:
            return {"id": self.id, "status": "ERROR", "output": str(e)}

    def report(self):
        """Generate a JSON report"""
        result = self.check()
        return json.dumps(result, indent=4)


# Ejemplo de uso
if __name__ == "__main__":
    control = control_1_2_1()
    print("=== CHECK ===")
    print(control.report())

    if control.check()["status"] == "FAIL":
        print("=== REMEDIATING ===")
        print(control.remediate())
