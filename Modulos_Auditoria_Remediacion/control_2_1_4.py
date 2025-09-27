import subprocess
import json
import glob

class control_2_1_4:
    def __init__(self):
        self.id = "2.1.4"
        self.title = "Ensure the autoindex module is disabled"
        self.description = "Verify that the autoindex directive is not set to 'on' in NGINX configuration files."

    def check(self):
        """Audit: search nginx.conf and conf.d/* for autoindex directives"""
        try:
            findings = []
            files = ["/etc/nginx/nginx.conf"] + glob.glob("/etc/nginx/conf.d/*.conf")

            for f in files:
                try:
                    with open(f, "r") as conf:
                        for line in conf:
                            if "autoindex" in line.lower():
                                findings.append(f"{f}: {line.strip()}")
                except FileNotFoundError:
                    continue

            if any("autoindex on" in entry.lower() for entry in findings):
                return {
                    "id": self.id,
                    "status": "FAIL",
                    "output": "\n".join(findings)
                }
            else:
                return {
                    "id": self.id,
                    "status": "PASS",
                    "output": "No autoindex enabled directives found"
                }
        except Exception as e:
            return {
                "id": self.id,
                "status": "ERROR",
                "output": str(e)
            }

    def remediate(self):
        """Remediation: disable autoindex by replacing 'autoindex on' with 'autoindex off'"""
        try:
            files = ["/etc/nginx/nginx.conf"] + glob.glob("/etc/nginx/conf.d/*.conf")
            changes = []

            for f in files:
                try:
                    with open(f, "r") as conf:
                        lines = conf.readlines()
                    new_lines = []
                    modified = False
                    for line in lines:
                        if "autoindex on" in line.lower():
                            new_lines.append("    autoindex off;\n")
                            modified = True
                            changes.append(f"Modified {f}: {line.strip()} -> autoindex off;")
                        else:
                            new_lines.append(line)
                    if modified:
                        with open(f, "w") as conf:
                            conf.writelines(new_lines)
                except FileNotFoundError:
                    continue

            # Recargar configuración de NGINX
            subprocess.run("systemctl reload nginx", shell=True, check=False)

            return {
                "id": self.id,
                "status": "REMEDIATED",
                "output": "\n".join(changes) if changes else "No changes needed (autoindex already disabled)"
            }
        except Exception as e:
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
    control = control_2_1_4()
    print("=== CHECK ===")
    print(control.report())

    if control.check()["status"] == "FAIL":
        print("=== REMEDIATING ===")
        print(control.remediate())
