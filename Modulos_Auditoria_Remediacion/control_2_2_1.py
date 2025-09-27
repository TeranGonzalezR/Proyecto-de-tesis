import subprocess
import json
import pwd
import grp

class control_2_2_1:
    def __init__(self):
        self.id = "2.2.1"
        self.title = "Ensure NGINX is run using a non-privileged, dedicated service account"
        self.description = "Verify that NGINX worker processes run under a dedicated non-privileged user."

    def check(self):
        """Audit: verify nginx runs as a non-privileged, dedicated user"""
        findings = []

        # 1. Revisar nginx.conf para encontrar directiva user
        try:
            with open("/etc/nginx/nginx.conf", "r") as conf:
                lines = conf.readlines()
                user_line = [line.strip() for line in lines if line.strip().startswith("user")]
                if user_line:
                    user_directive = user_line[0].split()[1].replace(";", "")
                    findings.append(f"User directive in nginx.conf: {user_directive}")
                else:
                    return {
                        "id": self.id,
                        "status": "FAIL",
                        "output": "No user directive found in /etc/nginx/nginx.conf"
                    }
        except FileNotFoundError:
            return {
                "id": self.id,
                "status": "ERROR",
                "output": "/etc/nginx/nginx.conf not found"
            }

        # 2. Verificar que el usuario exista
        try:
            user_info = pwd.getpwnam(user_directive)
            findings.append(f"User {user_directive} exists with UID {user_info.pw_uid}")
            if user_info.pw_uid == 0:
                return {
                    "id": self.id,
                    "status": "FAIL",
                    "output": f"User {user_directive} is privileged (UID 0)"
                }
        except KeyError:
            return {
                "id": self.id,
                "status": "FAIL",
                "output": f"User {user_directive} not found in system"
            }

        # 3. Verificar grupos
        groups = [g.gr_name for g in grp.getgrall() if user_directive in g.gr_mem or g.gr_gid == user_info.pw_gid]
        if len(groups) > 1:
            findings.append(f"User {user_directive} belongs to multiple groups: {', '.join(groups)}")
            return {"id": self.id, "status": "FAIL", "output": "\n".join(findings)}
        else:
            findings.append(f"User {user_directive} only belongs to group {groups[0]}")

        return {"id": self.id, "status": "PASS", "output": "\n".join(findings)}

    def remediate(self):
        """Remediation: create dedicated nginx user and update nginx.conf"""
        try:
            # Crear grupo nginx si no existe
            try:
                grp.getgrnam("nginx")
            except KeyError:
                subprocess.run("groupadd nginx", shell=True, check=True)

            # Crear usuario nginx si no existe
            try:
                pwd.getpwnam("nginx")
            except KeyError:
                subprocess.run("useradd nginx -r -g nginx -d /var/cache/nginx -s /sbin/nologin", shell=True, check=True)

            # Modificar nginx.conf para usar "user nginx;"
            updated = False
            conf_file = "/etc/nginx/nginx.conf"
            with open(conf_file, "r") as conf:
                lines = conf.readlines()
            new_lines = []
            for line in lines:
                if line.strip().startswith("user"):
                    new_lines.append("user nginx;\n")
                    updated = True
                else:
                    new_lines.append(line)
            if not updated:
                new_lines.insert(0, "user nginx;\n")
            with open(conf_file, "w") as conf:
                conf.writelines(new_lines)

            # Recargar NGINX
            subprocess.run("systemctl reload nginx", shell=True, check=False)

            return {
                "id": self.id,
                "status": "REMEDIATED",
                "output": "Dedicated user 'nginx' created and nginx.conf updated"
            }
        except subprocess.CalledProcessError as e:
            return {"id": self.id, "status": "ERROR", "output": str(e)}

    def report(self):
        """Generate JSON report"""
        result = self.check()
        return json.dumps(result, indent=4)


# Ejemplo de uso
if __name__ == "__main__":
    control = control_2_2_1()
    print("=== CHECK ===")
    print(control.report())

    if control.check()["status"] == "FAIL":
        print("=== REMEDIATING ===")
        print(control.remediate())
