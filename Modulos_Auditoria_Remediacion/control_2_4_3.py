import re
import glob
import os
import json
import subprocess

class control_2_4_3:
    def __init__(self):
        self.id = "2.4.3"
        self.title = "Ensure keepalive_timeout is 10 seconds or less, but not 0"
        self.description = "Verify that keepalive_timeout is configured correctly in nginx.conf."

    def find_keepalive_timeout(self):
        """Buscar la directiva keepalive_timeout en archivos de configuración"""
        files = ["/etc/nginx/nginx.conf"] + glob.glob("/etc/nginx/conf.d/*.conf")
        values = []
        for f in files:
            if not os.path.exists(f):
                continue
            with open(f, "r") as conf:
                for line in conf:
                    match = re.search(r"keepalive_timeout\s+(\d+)", line)
                    if match:
                        values.append((f, int(match.group(1)), line.strip()))
        return values

    def check(self):
        """Audit: verificar keepalive_timeout"""
        values = self.find_keepalive_timeout()
        if not values:
            return {
                "id": self.id,
                "status": "FAIL",
                "output": "keepalive_timeout not set (defaults to browser-controlled, insecure)"
            }

        findings = []
        for f, val, line in values:
            if val == 0 or val > 10:
                findings.append(f"{f}: {line}")

        if findings:
            return {
                "id": self.id,
                "status": "FAIL",
                "output": "Invalid keepalive_timeout found:\n" + "\n".join(findings)
            }
        else:
            return {
                "id": self.id,
                "status": "PASS",
                "output": "All keepalive_timeout values are ≤ 10 and not 0"
            }

    def remediate(self):
        """Remediation: set keepalive_timeout to 10 in nginx.conf"""
        conf_file = "/etc/nginx/nginx.conf"
        if not os.path.exists(conf_file):
            return {
                "id": self.id,
                "status": "ERROR",
                "output": f"{conf_file} not found"
            }

        try:
            with open(conf_file, "r") as conf:
                lines = conf.readlines()

            updated = False
            new_lines = []
            for line in lines:
                if "keepalive_timeout" in line and not line.strip().startswith("#"):
                    new_lines.append("    keepalive_timeout 10;\n")
                    updated = True
                else:
                    new_lines.append(line)

            if not updated:
                # Insertar dentro del bloque http { }
                for i, line in enumerate(new_lines):
                    if line.strip().startswith("http {"):
                        new_lines.insert(i + 1, "    keepalive_timeout 10;\n")
                        updated = True
                        break

            with open(conf_file, "w") as conf:
                conf.writelines(new_lines)

            subprocess.run("systemctl reload nginx", shell=True, check=False)

            return {
                "id": self.id,
                "status": "REMEDIATED",
                "output": "keepalive_timeout set to 10 in nginx.conf and nginx reloaded"
            }

        except Exception as e:
            return {
                "id": self.id,
                "status": "ERROR",
                "output": str(e)
            }

    def report(self):
        """Generar reporte en JSON"""
        result = self.check()
        return json.dumps(result, indent=4)


# Ejemplo de uso
if __name__ == "__main__":
    control = control_2_4_3()
    print("=== CHECK ===")
    print(control.report())

    if control.check()["status"] == "FAIL":
        print("=== REMEDIATING ===")
        print(control.remediate())
