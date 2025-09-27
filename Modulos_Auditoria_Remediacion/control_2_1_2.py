import subprocess
import json

class control_2_1_2:
    def __init__(self):
        self.id = "2.1.2"
        self.title = "Ensure HTTP WebDAV module is not installed"
        self.description = "Verify that the http_dav_module is not compiled into NGINX."

    def check(self):
        """Audit: verify nginx is not compiled with http_dav_module"""
        try:
            result = subprocess.run(
                "nginx -V 2>&1 | grep http_dav_module",
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True
            )
            if result.stdout.strip() == "":
                return {
                    "id": self.id,
                    "status": "PASS",
                    "output": "http_dav_module not found"
                }
            else:
                return {
                    "id": self.id,
                    "status": "FAIL",
                    "output": "http_dav_module detected"
                }
        except FileNotFoundError:
            return {
                "id": self.id,
                "status": "ERROR",
                "output": "nginx command not found"
            }

    def remediate(self):
        """Remediation: recompile nginx without http_dav_module"""
        try:
            version = "1.26.1"
            url = f"http://nginx.org/download/nginx-{version}.tar.gz"
            commands = [
                "dnf install -y gcc make wget tar zlib-devel pcre-devel openssl-devel",
                f"wget {url} -O /tmp/nginx.tar.gz",
                "cd /tmp && tar -xvf nginx.tar.gz",
                f"cd /tmp/nginx-{version} && ./configure --with-http_ssl_module --without-http_dav_module",
                f"cd /tmp/nginx-{version} && make",
                f"cd /tmp/nginx-{version} && make install"
            ]

            for cmd in commands:
                subprocess.run(cmd, shell=True, check=True)

            return {
                "id": self.id,
                "status": "REMEDIATED",
                "output": f"NGINX {version} recompiled without http_dav_module"
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
    control = control_2_1_2()
    print("=== CHECK ===")
    print(control.report())

    if control.check()["status"] == "FAIL":
        print("=== REMEDIATING ===")
        print(control.remediate())
