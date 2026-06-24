import subprocess
from config.config import APP_MAP
import psutil
import os


class AppManager:

    def __init__(self):
        self.apps = APP_MAP

        # app_name -> {process, pid, path}
        self.open_apps = {}
    def open_app(self, app_name):

        app_name = app_name.lower()

        # check real OS state first
        existing = self.get_process_by_name(app_name)

        if existing:
            print(f"{app_name} already running (PID: {existing.pid})")
            self.open_apps[app_name] = existing
            return

        path = self.apps.get(app_name)

        if not path:
            print(f"{app_name} not found")
            return
        if path.startswith("steam://"):
            process = os.startfile(path)
        else:
            process = subprocess.Popen(path)

        self.open_apps[app_name] = process

        print(f"Opened {app_name} (PID: {process.pid})")
    def get_process_by_name(self, name):
        """Find real running process in OS"""
        name = name.lower()

        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if proc.info['name'] and proc.info['name'].lower() == f"{name}.exe":
                    return proc
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        return None

    def close_app(self, app_name):

        app_name = app_name.lower()

        proc = self.get_process_by_name(app_name)

        if not proc:
            print(f"{app_name} not running in OS")
            self.open_apps.pop(app_name, None)
            return

        try:
            print(f"Closing {app_name} (PID: {proc.pid})")

            proc.terminate()
            proc.wait(timeout=5)

        except Exception:
            proc.kill()

        self.open_apps.pop(app_name, None)

        print(f"{app_name} closed")