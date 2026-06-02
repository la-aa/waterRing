import ctypes
import math
import random
import sys
import tkinter as tk
from datetime import datetime, timedelta
from typing import Optional

from .config import AppConfig
from .startup import is_enabled as startup_is_enabled
from .startup import set_enabled as startup_set_enabled
from .tray import WinTrayIcon, is_windows


APP_TITLE = "Water Ring"

if is_windows():
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass


class WaterRingAssistant:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title(APP_TITLE)
        self.root.geometry("330x210")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.withdraw()

        self.config = AppConfig(auto_start=startup_is_enabled())
        self.active = False
        self.sparkle_phase = 0.0
        self.blink = True
        self.pulse = 0
        self.drag_offset = (0, 0)
        self.settings_window: Optional[tk.Toplevel] = None
        self.tray = WinTrayIcon(self.show, self.open_settings, self.exit_app) if is_windows() else None

        self._build_ui()
        self._place_bottom_right()
        self._bind_events()
        self._sync_next_reminder()

        if self.config.auto_start and self.tray:
            self.tray.start()

        self.root.after(500, self._tick)
        self.root.protocol("WM_DELETE_WINDOW", self.hide)

    def _build_ui(self) -> None:
        self.frame = tk.Frame(self.root, bg="#FFF7FB", bd=1, relief="solid")
        self.frame.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(self.frame, width=330, height=145, bg="#FFF7FB", highlightthickness=0)
        self.canvas.pack(fill="x", side="top")

        bottom = tk.Frame(self.frame, bg="#FFF7FB")
        bottom.pack(fill="x", side="bottom", padx=10, pady=(0, 10))

        self.message_var = tk.StringVar(value="喵~ 记得喝水哦")
        self.message = tk.Label(bottom, textvariable=self.message_var, bg="#FFF7FB", fg="#5B4B55", font=("Microsoft YaHei UI", 10, "bold"))
        self.message.pack(anchor="w")

        controls = tk.Frame(bottom, bg="#FFF7FB")
        controls.pack(fill="x", pady=(8, 0))

        buttons = [
            ("我喝了", self.mark_drunk, "#FFB7C7", "white"),
            ("稍后提醒", self.snooze, "#B8D8FF", "#234"),
            ("设置", self.open_settings, "#DFF0D8", "#335"),
        ]
        for text, cmd, bg, fg in buttons:
            tk.Button(controls, text=text, command=cmd, bg=bg, fg=fg, activebackground=bg, activeforeground=fg, relief="flat", bd=0, font=("Microsoft YaHei UI", 9, "bold"), padx=10, pady=3).pack(side="left", padx=(0, 8))

        tk.Button(controls, text="×", command=self.hide, bg="#FFF7FB", fg="#7A6470", activebackground="#F2E7ED", activeforeground="#5B4B55", relief="flat", bd=0, font=("Segoe UI", 11, "bold"), padx=6, pady=0).pack(side="right")

    def _bind_events(self) -> None:
        for widget in (self.root, self.frame, self.canvas):
            widget.bind("<ButtonPress-1>", self._start_drag)
            widget.bind("<B1-Motion>", self._drag)
            widget.bind("<Double-Button-1>", self.toggle_idle)
        self.canvas.bind("<Button-1>", self._canvas_click)

    def _place_bottom_right(self) -> None:
        self.root.update_idletasks()
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = sw - 350
        y = sh - 260
        self.root.geometry(f"330x210+{x}+{y}")

    def _start_drag(self, event) -> None:
        self.drag_offset = (event.x_root - self.root.winfo_x(), event.y_root - self.root.winfo_y())

    def _drag(self, event) -> None:
        x = event.x_root - self.drag_offset[0]
        y = event.y_root - self.drag_offset[1]
        self.root.geometry(f"330x210+{x}+{y}")

    def _canvas_click(self, _event) -> None:
        if not self.active:
            self.show()
            return
        self.message_var.set(random.choice(["喵呜，快喝一口水", "补充水分，继续工作", "只要一小口也算"]))
        self.pulse = 10

    def _sync_next_reminder(self) -> None:
        self.config.next_reminder = datetime.now() + timedelta(minutes=self.config.interval_minutes)

    def toggle_idle(self, _event=None) -> None:
        if self.active:
            self.hide()
        else:
            self.show()

    def show(self) -> None:
        self.active = True
        self.root.deiconify()
        self.root.lift()
        self.root.attributes("-topmost", True)
        self.pulse = 10
        self.blink = True
        self._draw()

    def hide(self) -> None:
        self.active = False
        self.root.withdraw()

    def mark_drunk(self) -> None:
        self.config.next_reminder = datetime.now() + timedelta(minutes=self.config.interval_minutes)
        self.message_var.set("好，记下啦。下一次再来叫你。")
        self.root.after(1200, self.hide)

    def snooze(self) -> None:
        self.config.next_reminder = datetime.now() + timedelta(minutes=self.config.snooze_minutes)
        self.message_var.set("那我先安静一会儿，稍后再提醒你。")
        self.root.after(1000, self.hide)

    def _tick(self) -> None:
        now = datetime.now()
        if now >= self.config.next_reminder and not self.active:
            self.show()
            self.message_var.set("喵！该喝水啦。点我可以互动。")
            self.root.after(self.config.reminder_seconds * 1000, self._auto_hide)
        self.sparkle_phase = (self.sparkle_phase + 0.12) % (2 * math.pi)
        if self.active:
            self._draw()
            if self.pulse > 0:
                self.pulse -= 1
        self.root.after(500, self._tick)

    def _auto_hide(self) -> None:
        if self.active:
            self.hide()

    def _draw(self) -> None:
        c = self.canvas
        c.delete("all")
        self._draw_bg(c)
        self._draw_cat(c)
        self._draw_bubble(c)

    def _draw_bg(self, c: tk.Canvas) -> None:
        c.create_oval(15, 18, 115, 118, fill="#FFE8F0", outline="")
        c.create_oval(212, 18, 306, 112, fill="#E8F2FF", outline="")
        for i in range(5):
            x = 242 + i * 10
            y = 25 + int(3 * math.sin(self.sparkle_phase + i))
            c.create_text(x, y, text="✦", fill="#E6A8BC", font=("Segoe UI Symbol", 9, "bold"))

    def _draw_cat(self, c: tk.Canvas) -> None:
        x0, y0 = 72, 34
        face = "#F9D7B7" if self.config.cat_style == "classic" else "#F6E7D2"
        outline = "#CFA47D" if self.config.cat_style == "classic" else "#BFA98B"
        c.create_oval(x0, y0, x0 + 108, y0 + 92, fill=face, outline=outline, width=2)
        c.create_polygon(x0 + 10, y0 + 10, x0 + 25, y0 - 18, x0 + 41, y0 + 12, fill=face, outline=outline, width=2)
        c.create_polygon(x0 + 67, y0 + 12, x0 + 83, y0 - 18, x0 + 98, y0 + 10, fill=face, outline=outline, width=2)
        eye_y = y0 + 38
        if self.blink:
            c.create_line(x0 + 28, eye_y, x0 + 40, eye_y, fill="#5E4A40", width=3)
            c.create_line(x0 + 68, eye_y, x0 + 80, eye_y, fill="#5E4A40", width=3)
            self.blink = random.random() > 0.15
        else:
            c.create_oval(x0 + 26, eye_y - 6, x0 + 38, eye_y + 6, fill="#5E4A40", outline="")
            c.create_oval(x0 + 66, eye_y - 6, x0 + 78, eye_y + 6, fill="#5E4A40", outline="")
        c.create_line(x0 + 54, y0 + 45, x0 + 50, y0 + 55, x0 + 58, y0 + 55, smooth=True, fill="#8C6A58", width=2)
        c.create_line(x0 + 52, y0 + 58, x0 + 46, y0 + 62, fill="#D88FA8", width=2)
        c.create_line(x0 + 58, y0 + 58, x0 + 64, y0 + 62, fill="#D88FA8", width=2)
        if self.pulse:
            c.create_arc(x0 + 20, y0 + 20, x0 + 40, y0 + 40, start=45, extent=270, style="arc", outline="#FF9FB5", width=2)
            c.create_arc(x0 + 68, y0 + 20, x0 + 88, y0 + 40, start=45, extent=270, style="arc", outline="#FF9FB5", width=2)
        c.create_text(x0 + 54, y0 + 80, text="喵", fill="#7A5A48", font=("Microsoft YaHei UI", 14, "bold"))
        c.create_text(x0 + 54, y0 + 108, text="喝水时间到", fill="#6B5B66", font=("Microsoft YaHei UI", 9, "bold"))

    def _draw_bubble(self, c: tk.Canvas) -> None:
        bx1, by1, bx2, by2 = 186, 42, 310, 100
        c.create_polygon(
            bx1 + 12, by1,
            bx2 - 12, by1,
            bx2, by1 + 12,
            bx2, by2 - 12,
            bx2 - 12, by2,
            bx1 + 34, by2,
            bx1 + 22, by2 + 12,
            bx1 + 20, by2,
            bx1 + 12, by2,
            bx1, by2 - 12,
            bx1, by1 + 12,
            fill="#FFFFFF",
            outline="#D7DDEA",
            smooth=True,
        )
        c.create_text((bx1 + bx2) / 2, by1 + 24, text=random.choice(["该喝水啦", "补一口水，继续工作", "别忘了照顾自己"]), fill="#41505C", font=("Microsoft YaHei UI", 11, "bold"))
        c.create_text((bx1 + bx2) / 2, by1 + 48, text="点击小猫可互动", fill="#7A8793", font=("Microsoft YaHei UI", 8))

    def open_settings(self) -> None:
        if self.settings_window and self.settings_window.winfo_exists():
            self.settings_window.lift()
            return

        win = tk.Toplevel(self.root)
        win.title("设置")
        win.geometry("340x280")
        win.resizable(False, False)
        win.attributes("-topmost", True)
        win.configure(bg="#FFF7FB")
        self.settings_window = win

        interval_var = tk.IntVar(value=self.config.interval_minutes)
        snooze_var = tk.IntVar(value=self.config.snooze_minutes)
        seconds_var = tk.IntVar(value=self.config.reminder_seconds)
        autostart_var = tk.BooleanVar(value=self.config.auto_start)
        minimized_var = tk.BooleanVar(value=self.config.launch_minimized)
        style_var = tk.StringVar(value=self.config.cat_style)

        def row(label: str, widget: tk.Widget) -> None:
            frame = tk.Frame(win, bg="#FFF7FB")
            frame.pack(fill="x", padx=14, pady=6)
            tk.Label(frame, text=label, width=12, anchor="w", bg="#FFF7FB", fg="#4B4B58", font=("Microsoft YaHei UI", 9, "bold")).pack(side="left")
            widget.pack(side="left", fill="x", expand=True)

        row("提醒间隔", tk.Spinbox(win, from_=10, to=240, textvariable=interval_var, width=8))
        row("稍后提醒", tk.Spinbox(win, from_=3, to=120, textvariable=snooze_var, width=8))
        row("弹出停留", tk.Spinbox(win, from_=3, to=60, textvariable=seconds_var, width=8))

        style_frame = tk.Frame(win, bg="#FFF7FB")
        style_frame.pack(fill="x", padx=14, pady=6)
        tk.Label(style_frame, text="猫咪风格", width=12, anchor="w", bg="#FFF7FB", fg="#4B4B58", font=("Microsoft YaHei UI", 9, "bold")).pack(side="left")
        tk.Radiobutton(style_frame, text="经典", variable=style_var, value="classic", bg="#FFF7FB").pack(side="left")
        tk.Radiobutton(style_frame, text="奶油", variable=style_var, value="cream", bg="#FFF7FB").pack(side="left", padx=(10, 0))

        tk.Checkbutton(win, text="开机自启", variable=autostart_var, bg="#FFF7FB").pack(anchor="w", padx=14, pady=(10, 0))
        tk.Checkbutton(win, text="启动后最小化到托盘", variable=minimized_var, bg="#FFF7FB").pack(anchor="w", padx=14, pady=(2, 0))

        def save() -> None:
            self.config.interval_minutes = int(interval_var.get())
            self.config.snooze_minutes = int(snooze_var.get())
            self.config.reminder_seconds = int(seconds_var.get())
            self.config.auto_start = bool(autostart_var.get())
            self.config.launch_minimized = bool(minimized_var.get())
            self.config.cat_style = style_var.get()
            startup_set_enabled(self.config.auto_start)
            self._sync_next_reminder()
            if self.config.launch_minimized:
                self.hide()
            self.message_var.set("设置已保存")
            win.destroy()

        btns = tk.Frame(win, bg="#FFF7FB")
        btns.pack(fill="x", padx=14, pady=16)
        tk.Button(btns, text="保存", command=save, bg="#FFB7C7", fg="white", relief="flat", padx=12, pady=4).pack(side="left")
        tk.Button(btns, text="取消", command=win.destroy, bg="#E8EDF3", fg="#334", relief="flat", padx=12, pady=4).pack(side="left", padx=8)
        tk.Button(btns, text="立即提醒", command=self.show, bg="#DFF0D8", fg="#335", relief="flat", padx=12, pady=4).pack(side="right")

    def exit_app(self) -> None:
        if self.tray:
            self.tray.stop()
        self.root.destroy()

    def run(self) -> None:
        if self.config.launch_minimized:
            self.hide()
        else:
            self.show()
        self.root.mainloop()
