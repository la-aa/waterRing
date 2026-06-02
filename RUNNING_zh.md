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

## 打包建议

后续如果要打包成可执行文件，建议继续保留 `water_ring.py` 作为入口文件，并从仓库根目录进行打包。
