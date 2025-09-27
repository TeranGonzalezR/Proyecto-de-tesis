import subprocess
import json
import logging
import os
from typing import Dict, Any

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class control_1_2_2:
    def __init__(self):
        self.id = "1.2.2"
        self.title = "Ensure the latest software package is installed"
        self.description = "Verify that the latest version of NGINX is installed."

    def _run_command(self, cmd: list, check: bool = False) -> subprocess.CompletedProcess:
        """Ejecutar comando de forma segura"""
        try:
            return subprocess.run(
                cmd,
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE,
                universal_newlines=True,
                check=check,
                timeout=30  # Timeout de seguridad
            )
        except subprocess.TimeoutExpired:
            raise Exception(f"Command timed out: {' '.join(cmd)}")
        except subprocess.CalledProcessError as e:
            raise Exception(f"Command failed: {e}")
        except FileNotFoundError:
            raise Exception(f"Command not found: {cmd[0]}")

    def _check_root_privileges(self) -> bool:
        """Verificar si se tienen privilegios de root"""
        return os.geteuid() == 0

    def check(self) -> Dict[str, Any]:
        """Audit: check if nginx is at latest version"""
        try:
            logger.info(f"Checking NGINX package status for control {self.id}")
            
            # Verificar información del paquete instalado
            result_info = self._run_command(["dnf", "info", "nginx"])
            
            if result_info.returncode != 0:
                return {
                    "id": self.id,
                    "status": "FAIL",
                    "output": "NGINX package not installed",
                    "details": result_info.stderr.strip()
                }
            
            # Verificar actualizaciones disponibles
            result_update = self._run_command(["dnf", "check-update", "nginx"])
            
            # dnf check-update retorna 100 si hay actualizaciones disponibles
            if result_update.returncode == 100:
                return {
                    "id": self.id,
                    "status": "FAIL",
                    "output": "NGINX update available",
                    "details": result_update.stdout.strip(),
                    "current_info": result_info.stdout.strip()
                }
            elif result_update.returncode == 0:
                return {
                    "id": self.id,
                    "status": "PASS",
                    "output": "NGINX is up to date",
                    "current_info": result_info.stdout.strip()
                }
            else:
                return {
                    "id": self.id,
                    "status": "ERROR",
                    "output": "Failed to check for updates",
                    "details": result_update.stderr.strip()
                }
                
        except Exception as e:
            logger.error(f"Error during check: {e}")
            return {
                "id": self.id,
                "status": "ERROR",
                "output": str(e)
            }

    def remediate(self) -> Dict[str, Any]:
        """Remediation: update nginx package"""
        try:
            logger.info(f"Starting remediation for control {self.id}")
            
            # Verificar privilegios de root
            if not self._check_root_privileges():
                return {
                    "id": self.id,
                    "status": "ERROR",
                    "output": "Root privileges required for package updates"
                }
            
            # Actualizar el paquete
            result = self._run_command(["dnf", "update", "-y", "nginx"], check=True)
            
            logger.info("NGINX package updated successfully")
            return {
                "id": self.id,
                "status": "REMEDIATED",
                "output": "NGINX package updated successfully",
                "details": result.stdout.strip()
            }
            
        except Exception as e:
            logger.error(f"Error during remediation: {e}")
            return {
                "id": self.id,
                "status": "ERROR",
                "output": f"Remediation failed: {str(e)}"
            }

    def report(self) -> str:
        """Generate a JSON report"""
        try:
            result = self.check()
            return json.dumps(result, indent=4)
        except Exception as e:
            error_result = {
                "id": self.id,
                "status": "ERROR",
                "output": f"Report generation failed: {str(e)}"
            }
            return json.dumps(error_result, indent=4)

    def full_audit(self) -> Dict[str, Any]:
        """Ejecutar auditoría completa con remediación opcional"""
        check_result = self.check()
        
        if check_result["status"] == "FAIL":
            logger.info("Check failed, attempting remediation...")
            remediation_result = self.remediate()
            
            # Verificar nuevamente después de la remediación
            if remediation_result["status"] == "REMEDIATED":
                final_check = self.check()
                return {
                    "initial_check": check_result,
                    "remediation": remediation_result,
                    "final_check": final_check,
                    "overall_status": final_check["status"]
                }
            else:
                return {
                    "initial_check": check_result,
                    "remediation": remediation_result,
                    "overall_status": "FAILED_REMEDIATION"
                }
        
        return {
            "initial_check": check_result,
            "overall_status": check_result["status"]
        }


# Ejemplo de uso
if __name__ == "__main__":
    control = control_1_2_2()
    
    print("=== NGINX PACKAGE CONTROL ===")
    print(f"ID: {control.id}")
    print(f"Title: {control.title}")
    print(f"Description: {control.description}")
    print()
    
    print("=== BASIC CHECK ===")
    print(control.report())
    print()
    
    print("=== FULL AUDIT (with auto-remediation) ===")
    full_result = control.full_audit()
    print(json.dumps(full_result, indent=4))