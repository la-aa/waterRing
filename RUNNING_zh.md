# waterRing 运行说明

这是一个基于 Python 和 Tkinter 的 Windows 桌面喝水提醒小助手。

## 运行环境

- Windows 10 或 Windows 11
- Python 3.10 及以上
- 安装时带有 Tkinter 的 Python 发行版

## 克隆并运行

```bash
git clone <你的仓库地址>
cd waterRing
python water_ring.py
```

## 启动入口

- 推荐直接运行 `water_ring.py`
- 应用主入口位于 `water_ring_app/main.py`

## 打包成 exe

如果你不想再运行 `.py` 文件，可以把项目打包成 Windows 可执行程序。

先安装 PyInstaller：

```bash
pip install pyinstaller
```

然后在项目根目录执行：

```powershell
.\build.ps1
```

打包完成后，`exe` 会生成在 `dist\\waterRing.exe`。

项目会优先读取 `ico\\myCat_ico.jpg` 作为窗口图标，并在打包时自动转换为 `ico\\myCat_ico.ico` 用作 `exe` 图标。后期你只要替换这张图片即可。

## 功能说明

- 按设定时间提醒喝水
- 右下角弹出可爱的猫咪提醒窗
- 支持托盘常驻
- 支持设置提醒间隔、稍后提醒、弹窗停留时间、猫咪风格和自启
- 支持 Windows 开机自启注册

## 注意事项

- 托盘和开机自启功能仅适用于 Windows
- 项目不依赖第三方库，直接使用系统自带的 Tkinter
- 如果启动后没有看到窗口，检查是否已经最小化到托盘
- 如果打包成 `exe`，开机自启会自动指向 `exe` 本身，不再依赖 `py` 文件
- 如果程序启动失败，错误会写入 `logs\\app.log`

## 打包建议

后续如果要打包成可执行文件，建议继续保留 `water_ring.py` 作为入口文件，并从仓库根目录进行打包。
