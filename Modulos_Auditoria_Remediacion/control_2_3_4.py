import os
import stat
import pwd
import grp
import json

class control_2_3_4:
    def __init__(self):
        self.id = "2.3.4"
        self.title = "Ensure the core dump directory is secured"
        self.description = "Verify that the working_directory directive is properly secured."

    def get_working_directory(self):
        """Buscar la directiva working_directory en nginx.conf"""
        try:
            with open("/etc/nginx/nginx.conf", "r") as conf:
                for line in conf:
                    if "working_directory" in line and not line.strip().startswith("#"):
                        parts = line.strip().split()
                        if len(parts) >= 2:
                            return parts[1].replace(";", "")
        except FileNotFoundError:
            return None
        return None

    def check(self):
        """Audit: verificar el directorio de working_directory"""
        wdir = self.get_working_directory()
        if not wdir:
            return {
                "id": self.id,
                "status": "PASS",
                "output": "No working_directory directive found (default: disabled)"
            }

        if not os.path.exists(wdir):
            return {
                "id": self.id,
                "status": "FAIL",
                "output": f"Configured working_directory {wdir} does not exist"
            }

        st = os.stat(wdir)
        owner = pwd.getpwuid(st.st_uid).pw_name
        group = grp.getgrgid(st.st_gid).gr_name
        mode = stat.S_IMODE(st.st_mode)

        findings = []
        if owner != "root":
            findings.append(f"Owner is {owner}, expected root")
        if group != "nginx":
            findings.append(f"Group is {group}, expected nginx")
        if mode & 0o007:  # permisos para others
            findings.append(f"Directory {wdir} has others permissions: {oct(mode)}")

        if findings:
            return {
                "id": self.id,
                "status": "FAIL",
                "output": "\n".join(findings)
            }
        else:
            return {
                "id": self.id,
                "status": "PASS",
                "output": f"working_directory {wdir} is properly secured"
            }

    def remediate(self):
        """Remediation: ajustar permisos de working_directory"""
        wdir = self.get_working_directory()
        if not wdir:
            return {
                "id": self.id,
                "status": "INFO",
                "output": "No working_directory directive found (nothing to remediate)"
            }
        if not os.path.exists(wdir):
            return {
                "id": self.id,
                "status": "ERROR",
                "output": f"Configured working_directory {wdir} does not exist"
            }

        try:
            os.chown(wdir, pwd.getpwnam("root").pw_uid, grp.getgrnam("nginx").gr_gid)
            os.chmod(wdir, 0o750)  # root + group, no others
            return {
                "id": self.id,
                "status": "REMEDIATED",
                "output": f"working_directory {wdir} secured (owner root:nginx, perms 750)"
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
    control = control_2_3_4()
    print("=== CHECK ===")
    print(control.report())

    if control.check()["status"] == "FAIL":
        print("=== REMEDIATING ===")
        print(control.remediate())
