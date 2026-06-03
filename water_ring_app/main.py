from tkinter import messagebox

from .app import WaterRingAssistant
from .logger import write_exception


def main() -> None:
    try:
        app = WaterRingAssistant()
        app.run()
    except Exception as exc:
        write_exception(exc)
        try:
            messagebox.showerror(
                "Water Ring 启动失败",
                "程序启动失败，错误已写入 logs/app.log。\n请把日志内容发给我，我继续帮你定位。",
            )
        except Exception:
            pass
