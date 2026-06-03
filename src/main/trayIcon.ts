import path from "node:path";
import { app, Menu, Tray, nativeImage, type BrowserWindow } from "electron";

export function createTray(mainWindow: BrowserWindow) {
  const iconPath = path.join(app.getAppPath(), "ico/myCat_ico.jpg");
  const tray = new Tray(nativeImage.createFromPath(iconPath).resize({ width: 18, height: 18 }));
  tray.setToolTip("waterRing");
  tray.setContextMenu(
    Menu.buildFromTemplate([
      { label: "显示小助手", click: () => mainWindow.show() },
      { label: "隐藏", click: () => mainWindow.hide() },
      { type: "separator" },
      { label: "退出", click: () => app.quit() }
    ])
  );
  tray.on("double-click", () => mainWindow.show());
  return tray;
}
