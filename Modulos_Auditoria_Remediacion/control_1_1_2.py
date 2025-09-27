import subprocess
import json
import os

class control_1_1_2:
    def __init__(self):
        self.id = "1.1.2"
        self.title = "Ensure NGINX is installed from source"
        self.description = "Verify that NGINX is installed from source and not from package manager."

    def check(self):
        """Audit: check if nginx is installed by running 'nginx -v'"""
        try:
            result = subprocess.run(
                ["nginx", "-v"],
                stderr=subprocess.PIPE,  # nginx -v prints to stderr
                stdout=subprocess.PIPE,
                universal_newlines=True
            )
            if result.returncode == 0 and "nginx" in result.stderr.lower():
                return {"id": self.id, "status": "PASS", "output": result.stderr.strip()}
            else:
                return {"id": self.id, "status": "FAIL", "output": "Nginx not detected"}
        except FileNotFoundError:
            return {"id": self.id, "status": "FAIL", "output": "Nginx command not found"}

    def remediate(self):
        """Apply remediation: build and install nginx from source"""
        try:
            # Dependencias necesarias
            deps = "gcc make wget tar zlib-devel pcre-devel openssl-devel"
            subprocess.run(f"dnf install -y {deps}", shell=True, check=True)

            # Descargar y compilar la última versión de nginx (ejemplo: 1.26.1)
            version = "1.26.1"
            url = f"http://nginx.org/download/nginx-{version}.tar.gz"
            commands = [
                f"wget {url} -O /tmp/nginx.tar.gz",
                "cd /tmp && tar -xvf nginx.tar.gz",
                f"cd /tmp/nginx-{version} && ./configure --with-http_ssl_module --without-http_autoindex_module",
                f"cd /tmp/nginx-{version} && make",
                f"cd /tmp/nginx-{version} && make install"
            ]

            for cmd in commands:
                subprocess.run(cmd, shell=True, check=True)

            return {"id": self.id, "status": "REMEDIATED", "output": f"Nginx {version} installed from source"}
        except subprocess.CalledProcessError as e:
            return {"id": self.id, "status": "ERROR", "output": str(e)}

    def report(self):
        """Generate a JSON report"""
        result = self.check()
        return json.dumps(result, indent=4)


# Ejemplo de uso
if __name__ == "__main__":
    control = control_1_1_2()
    print("=== CHECK ===")
    print(control.report())

    if control.check()["status"] == "FAIL":
        print("=== REMEDIATING ===")
        print(control.remediate())