import subprocess
import json

class control_2_1_1:
    def __init__(self):
        self.id = "2.1.1"
        self.title = "Ensure only required modules are installed"
        self.description = "Audit NGINX to verify only the necessary modules are installed."

    def check(self):
        """Audit: list all modules included in NGINX build"""
        try:
            result = subprocess.run(
                "nginx -V",
                shell=True,
                stderr=subprocess.STDOUT,
                stdout=subprocess.PIPE,
                universal_newlines=True
            )
            if result.returncode == 0:
                return {
                    "id": self.id,
                    "status": "PASS",
                    "output": result.stdout.strip()
                }
            else:
                return {
                    "id": self.id,
                    "status": "FAIL",
                    "output": "Failed to retrieve NGINX build info"
                }
        except FileNotFoundError:
            return {
                "id": self.id,
                "status": "ERROR",
                "output": "nginx command not found"
            }

    def remediate(self):
        """Manual remediation guidance"""
        return {
            "id": self.id,
            "status": "MANUAL",
            "output": (
                "Review the output of 'nginx -V' and identify unnecessary modules.\n"
                "Recompile NGINX from source using './configure' without the unwanted modules.\n"
                "Example:\n"
                "  ./configure --with-http_ssl_module --without-http_autoindex_module\n"
                "  make && make install\n"
                "Consult the NGINX documentation for available module flags."
            )
        }

    def report(self):
        """Generate a JSON report"""
        result = self.check()
        return json.dumps(result, indent=4)


# Ejemplo de uso
if __name__ == "__main__":
    control = control_2_1_1()
    print("=== CHECK ===")
    print(control.report())

    print("=== REMEDIATION GUIDANCE ===")
    print(control.remediate())
