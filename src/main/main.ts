import { app, BrowserWindow, ipcMain, nativeImage } from "electron";
import { fileURLToPath } from "node:url";
import { mkdirSync } from "node:fs";
import path from "node:path";
import { getBottomRightBounds } from "./displayPosition";
import { setAutoStart } from "./loginItem";
import { settingsStore } from "./settingsStore";
import { createTray } from "./trayIcon";

let mainWindow: BrowserWindow | null = null;
let tray: ReturnType<typeof createTray> | null = null;
let reminderTimer: NodeJS.Timeout | null = null;
const __dirname = path.dirname(fileURLToPath(import.meta.url));
const userDataRoot = path.join(app.getPath("appData"), "waterRing");
const appRoot = app.getAppPath();

mkdirSync(path.join(userDataRoot, "Cache"), { recursive: true });
app.commandLine.appendSwitch("user-data-dir", userDataRoot);
app.commandLine.appendSwitch("disable-gpu");
app.commandLine.appendSwitch("disable-gpu-compositing");
app.setPath("userData", userDataRoot);
app.setPath("cache", path.join(userDataRoot, "Cache"));

function getPreloadPath() {
  return app.isPackaged
    ? path.join(process.resourcesPath, "out/preload/index.mjs")
    : path.join(appRoot, "out/preload/index.mjs");
}

function getIconPath() {
  return app.isPackaged
    ? path.join(process.resourcesPath, "ico/myCat_ico.jpg")
    : path.join(appRoot, "ico/myCat_ico.jpg");
}

function syncReminderTimer() {
  if (reminderTimer) {
    clearInterval(reminderTimer);
    reminderTimer = null;
  }

  reminderTimer = setInterval(() => {
    const nextReminderAt = settingsStore.getNextReminderAt();
    if (Date.now() >= nextReminderAt) {
      if (mainWindow && !mainWindow.isVisible()) {
        mainWindow.show();
      }
      mainWindow?.webContents.send("reminder:show");
    }
  }, 1000);
}

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 360,
    height: 220,
    show: false,
    frame: false,
    resizable: false,
    transparent: false,
    alwaysOnTop: true,
    skipTaskbar: true,
    backgroundColor: "#FFF7FB",
    icon: nativeImage.createFromPath(getIconPath()),
    webPreferences: {
      preload: getPreloadPath(),
      contextIsolation: true,
      nodeIntegration: false
    }
  });

  const { x, y } = getBottomRightBounds(360, 220);
  mainWindow.setPosition(x, y, false);

  if (!app.isPackaged) {
    mainWindow.loadURL("http://localhost:5173");
  } else {
  mainWindow.loadFile(path.join(appRoot, "out/renderer/index.html"));
  }

  mainWindow.webContents.once("did-finish-load", () => {
    console.log("waterRing preload path:", getPreloadPath());
    mainWindow?.webContents.executeJavaScript("Boolean(window.waterRing)").then((hasBridge) => {
      console.log("waterRing has bridge:", hasBridge);
    });
  });

  mainWindow.on("close", () => {
    mainWindow?.hide();
  });

  tray = createTray(mainWindow);

  const settings = settingsStore.getSettings();
  setAutoStart(settings.autoStart);
  syncReminderTimer();
  if (!settings.launchMinimized) {
    mainWindow.show();
  } else {
    mainWindow.hide();
  }
}

app.whenReady().then(() => {
  createWindow();

  ipcMain.handle("settings:get", () => settingsStore.getSettings());
  ipcMain.handle("settings:set", (_event, next) => {
    const merged = settingsStore.setSettings(next);
    setAutoStart(merged.autoStart);
    syncReminderTimer();
    return merged;
  });
  ipcMain.handle("reminder:snooze", () => {
    const next = Date.now() + settingsStore.getSettings().snoozeMinutes * 60_000;
    settingsStore.setNextReminderAt(next);
    return next;
  });
  ipcMain.handle("reminder:confirm", () => {
    const next = Date.now() + settingsStore.getSettings().intervalMinutes * 60_000;
    settingsStore.setNextReminderAt(next);
    return next;
  });
  ipcMain.handle("reminder:getNext", () => settingsStore.getNextReminderAt());
});

app.on("activate", () => {
  if (!mainWindow) {
    createWindow();
  } else {
    mainWindow.show();
  }
});

app.on("before-quit", () => {
  if (reminderTimer) {
    clearInterval(reminderTimer);
  }
});
