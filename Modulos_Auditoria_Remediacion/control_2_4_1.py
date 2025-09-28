import os
import re
import glob
import json

class control_2_4_1:
    def __init__(self, authorized_ports=None):
        self.id = "2.4.1"
        self.title = "Ensure NGINX only listens for network connections on authorized ports"
        self.description = "Verify that NGINX is only listening on authorized ports."
        self.authorized_ports = authorized_ports if authorized_ports else [80, 443]

    def find_listen_directives(self):
        """Buscar todas las directivas listen en la configuración"""
        files = ["/etc/nginx/nginx.conf"] + glob.glob("/etc/nginx/conf.d/*.conf")
        directives = []
        for f in files:
            if not os.path.exists(f):
                continue
            try:
                with open(f, "r") as conf:
                    for line in conf:
                        match = re.search(r"listen\s+(\d+)", line)
                        if match:
                            port = int(match.group(1))
                            directives.append((f, line.strip(), port))
            except Exception:
                continue
        return directives

    def check(self):
        """Audit: verificar que solo se escuchen puertos autorizados"""
        directives = self.find_listen_directives()
        unauthorized = [f"{f}: {line}" for f, line, port in directives if port not in self.authorized_ports]

        if unauthorized:
            return {
                "id": self.id,
                "status": "FAIL",
                "output": "Found unauthorized listening ports:\n" + "\n".join(unauthorized)
            }
        else:
            return {
                "id": self.id,
                "status": "PASS",
                "output": "All listening ports are authorized (" + ", ".join(map(str, self.authorized_ports)) + ")"
            }

    def remediate(self):
        """Remediation is manual (inform user what to change)"""
        return {
            "id": self.id,
            "status": "MANUAL",
            "output": "Please edit /etc/nginx/*.conf files and remove/comment out unauthorized listen directives, then run: systemctl reload nginx"
        }

    def report(self):
        """Generate JSON report"""
        result = self.check()
        return json.dumps(result, indent=4)


# Ejemplo de uso
if __name__ == "__main__":
    control = control_2_4_1(authorized_ports=[80, 443])  # puedes cambiar la lista
    print("=== CHECK ===")
    print(control.report())

    if control.check()["status"] == "FAIL":
        print("=== REMEDIATION REQUIRED ===")
        print(control.remediate())
