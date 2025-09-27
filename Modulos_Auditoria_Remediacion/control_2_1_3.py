import subprocess
import json

class control_2_1_3:
    def __init__(self):
        self.id = "2.1.3"
        self.title = "Ensure modules with gzip functionality are disabled"
        self.description = "Verify that http_gzip_module and http_gzip_static_module are not compiled into NGINX."

    def check(self):
        """Audit: verify gzip modules are not present"""
        try:
            result = subprocess.run(
                "nginx -V 2>&1 | grep -E '(http_gzip_module|http_gzip_static_module)'",
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True
            )
            if result.stdout.strip() == "":
                return {
                    "id": self.id,
                    "status": "PASS",
                    "output": "No gzip modules found"
                }
            else:
                return {
                    "id": self.id,
                    "status": "FAIL",
                    "output": f"Gzip modules detected:\n{result.stdout.strip()}"
                }
        except FileNotFoundError:
            return {
                "id": self.id,
                "status": "ERROR",
                "output": "nginx command not found"
            }

    def remediate(self):
        """Remediation: recompile nginx without gzip modules"""
        try:
            version = "1.26.1"
            url = f"http://nginx.org/download/nginx-{version}.tar.gz"
            commands = [
                "dnf install -y gcc make wget tar zlib-devel pcre-devel openssl-devel",
                f"wget {url} -O /tmp/nginx.tar.gz",
                "cd /tmp && tar -xvf nginx.tar.gz",
                f"cd /tmp/nginx-{version} && ./configure --with-http_ssl_module --without-http_gzip_module --without-http_gzip_static_module",
                f"cd /tmp/nginx-{version} && make",
                f"cd /tmp/nginx-{version} && make install"
            ]

            for cmd in commands:
                subprocess.run(cmd, shell=True, check=True)

            return {
                "id": self.id,
                "status": "REMEDIATED",
                "output": f"NGINX {version} recompiled without gzip modules"
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
    control = control_2_1_3()
    print("=== CHECK ===")
    print(control.report())

    if control.check()["status"] == "FAIL":
        print("=== REMEDIATING ===")
        print(control.remediate())
