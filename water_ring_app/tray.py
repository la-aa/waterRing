import ctypes
import sys

from .logger import write_exception


def is_windows() -> bool:
    return sys.platform.startswith("win")


class WinTrayIcon:
    WM_TRAY = ctypes.windll.user32.RegisterWindowMessageW("WATER_RING_TRAY")
    WM_TASKBARCREATED = ctypes.windll.user32.RegisterWindowMessageW("TaskbarCreated")
    NIM_ADD = 0
    NIM_DELETE = 2
    NIF_MESSAGE = 0x1
    NIF_ICON = 0x2
    NIF_TIP = 0x4
    WM_LBUTTONUP = 0x0202
    WM_RBUTTONUP = 0x0205
    WM_COMMAND = 0x0111
    TPM_RIGHTBUTTON = 0x0002
    TPM_RETURNCMD = 0x0100
    MF_STRING = 0x0000
    MF_SEPARATOR = 0x0800
    ID_OPEN = 1001
    ID_SETTINGS = 1002
    ID_EXIT = 1003

    class NOTIFYICONDATAW(ctypes.Structure):
        _fields_ = [
            ("cbSize", ctypes.c_ulong),
            ("hWnd", ctypes.c_void_p),
            ("uID", ctypes.c_uint),
            ("uFlags", ctypes.c_uint),
            ("uCallbackMessage", ctypes.c_uint),
            ("hIcon", ctypes.c_void_p),
            ("szTip", ctypes.c_wchar * 128),
            ("dwState", ctypes.c_uint),
            ("dwStateMask", ctypes.c_uint),
            ("szInfo", ctypes.c_wchar * 256),
            ("uTimeoutOrVersion", ctypes.c_uint),
            ("szInfoTitle", ctypes.c_wchar * 64),
            ("dwInfoFlags", ctypes.c_uint),
            ("guidItem", ctypes.c_byte * 16),
            ("hBalloonIcon", ctypes.c_void_p),
        ]

    def __init__(self, on_open, on_settings, on_exit):
        self.on_open = on_open
        self.on_settings = on_settings
        self.on_exit = on_exit
        self._hwnd = None
        self._nid = None
        self._wndproc = None
        self._thread = None
        self._running = False

    def start(self) -> None:
        if not is_windows() or self._running:
            return
        import threading

        self._running = True
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        if not is_windows() or not self._running:
            return
        self._running = False
        if self._hwnd:
            self._delete_icon()
            ctypes.windll.user32.PostMessageW(self._hwnd, 0x0012, 0, 0)

    def _run(self) -> None:
        try:
            user32 = ctypes.windll.user32
            kernel32 = ctypes.windll.kernel32
            WNDPROCTYPE = ctypes.WINFUNCTYPE(ctypes.c_longlong, ctypes.c_void_p, ctypes.c_uint, ctypes.c_uint64, ctypes.c_int64)

            def wndproc(hwnd, msg, wparam, lparam):
                if msg in (self.WM_TRAY, self.WM_TASKBARCREATED):
                    if lparam == self.WM_LBUTTONUP:
                        self.on_open()
                    elif lparam == self.WM_RBUTTONUP:
                        self._show_menu()
                    return 0
                if msg == self.WM_COMMAND:
                    cmd = wparam & 0xFFFF
                    if cmd == self.ID_OPEN:
                        self.on_open()
                    elif cmd == self.ID_SETTINGS:
                        self.on_settings()
                    elif cmd == self.ID_EXIT:
                        self.on_exit()
                    return 0
                if msg == 0x0010:
                    self._delete_icon()
                    user32.PostQuitMessage(0)
                    return 0
                return user32.DefWindowProcW(hwnd, msg, wparam, lparam)

            self._wndproc = WNDPROCTYPE(wndproc)
            class_name = "WaterRingTrayWindow"
            wndclass = ctypes.wintypes.WNDCLASSW()
            wndclass.lpfnWndProc = self._wndproc
            wndclass.hInstance = kernel32.GetModuleHandleW(None)
            wndclass.lpszClassName = class_name
            user32.RegisterClassW(ctypes.byref(wndclass))
            self._hwnd = user32.CreateWindowExW(0, class_name, class_name, 0, 0, 0, 0, 0, 0, 0, wndclass.hInstance, None)
            self._add_icon()

            msg = ctypes.wintypes.MSG()
            while user32.GetMessageW(ctypes.byref(msg), 0, 0, 0) != 0:
                user32.TranslateMessage(ctypes.byref(msg))
                user32.DispatchMessageW(ctypes.byref(msg))
        except Exception as exc:
            write_exception(exc)
            self.on_open()

    def _show_menu(self) -> None:
        user32 = ctypes.windll.user32
        menu = user32.CreatePopupMenu()
        user32.AppendMenuW(menu, self.MF_STRING, self.ID_OPEN, "显示小助手")
        user32.AppendMenuW(menu, self.MF_STRING, self.ID_SETTINGS, "设置")
        user32.AppendMenuW(menu, self.MF_SEPARATOR, 0, None)
        user32.AppendMenuW(menu, self.MF_STRING, self.ID_EXIT, "退出")
        user32.SetForegroundWindow(self._hwnd)
        pt = ctypes.wintypes.POINT()
        user32.GetCursorPos(ctypes.byref(pt))
        cmd = user32.TrackPopupMenu(menu, self.TPM_RETURNCMD | self.TPM_RIGHTBUTTON, pt.x, pt.y, 0, self._hwnd, None)
        if cmd:
            user32.PostMessageW(self._hwnd, self.WM_COMMAND, cmd, 0)
        user32.DestroyMenu(menu)

    def _add_icon(self) -> None:
        nid = self.NOTIFYICONDATAW()
        nid.cbSize = ctypes.sizeof(nid)
        nid.hWnd = self._hwnd
        nid.uID = 1
        nid.uFlags = self.NIF_MESSAGE | self.NIF_ICON | self.NIF_TIP
        nid.uCallbackMessage = self.WM_TRAY
        nid.hIcon = ctypes.windll.user32.LoadIconW(None, ctypes.c_int(32512))
        nid.szTip = "Water Ring - 右键退出"
        ctypes.windll.shell32.Shell_NotifyIconW(self.NIM_ADD, ctypes.byref(nid))
        self._nid = nid

    def _delete_icon(self) -> None:
        if self._hwnd and self._nid:
            ctypes.windll.shell32.Shell_NotifyIconW(self.NIM_DELETE, ctypes.byref(self._nid))
