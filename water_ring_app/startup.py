from pathlib import Path
import sys


APP_NAME = "WaterRing"
RUN_KEY = r"Software\Microsoft\Windows\CurrentVersion\Run"


def is_windows() -> bool:
    return sys.platform.startswith("win")


def is_enabled() -> bool:
    if not is_windows():
        return False
    try:
        import winreg

        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, RUN_KEY) as key:
            winreg.QueryValueEx(key, APP_NAME)
            return True
    except Exception:
        return False


def set_enabled(enabled: bool) -> None:
    if not is_windows():
        return
    try:
        import winreg

        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, RUN_KEY, 0, winreg.KEY_SET_VALUE) as key:
            if enabled:
                exe = Path(sys.executable)
                script = Path(__file__).resolve().parents[1] / "water_ring.py"
                value = f'"{exe}" "{script}"'
                winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, value)
            else:
                try:
                    winreg.DeleteValue(key, APP_NAME)
                except FileNotFoundError:
                    pass
    except Exception:
        pass
