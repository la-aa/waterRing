# waterRing

一个 Windows 桌面喝水提醒小助手，使用 Python + Tkinter 实现。项目已经整理成可提交到 GitHub 的结构，不再依赖单文件。

## 运行

```bash
python water_ring.py
```

## 目录

- `water_ring.py`：兼容入口，直接运行这个文件即可
- `water_ring_app/`：核心应用代码
  - `app.py`：主界面、提醒逻辑、设置窗口
  - `tray.py`：Windows 托盘图标和右键菜单
  - `startup.py`：开机自启
  - `config.py`：配置数据结构
  - `main.py`：应用入口

## 功能

- 定时提醒喝水
- 右下角弹出小猫提醒窗
- 点击互动
- 托盘图标支持显示、设置、退出
- 开机自启
- 启动后最小化到托盘
- 可调整提醒间隔、稍后提醒、弹窗停留时间
- 可切换猫咪风格

## 默认设置

- 提醒间隔：60 分钟
- 稍后提醒：15 分钟
- 弹窗停留：10 秒

## 说明

- 该项目目前以 Windows 为目标平台
- 托盘和自启功能依赖 Windows API
- 项目没有第三方依赖，直接用系统自带的 Tkinter
