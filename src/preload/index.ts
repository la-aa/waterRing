import { contextBridge, ipcRenderer } from "electron";

contextBridge.exposeInMainWorld("waterRing", {
  getSettings: () => ipcRenderer.invoke("settings:get"),
  setSettings: (next: unknown) => ipcRenderer.invoke("settings:set", next),
  confirmWater: () => ipcRenderer.invoke("reminder:confirm"),
  snooze: () => ipcRenderer.invoke("reminder:snooze"),
  getNextReminderAt: () => ipcRenderer.invoke("reminder:getNext"),
  onReminderShow: (callback: () => void) => {
    const handler = () => callback();
    ipcRenderer.on("reminder:show", handler);
    return () => ipcRenderer.removeListener("reminder:show", handler);
  }
});
