import { app } from "electron";

export function setAutoStart(enabled: boolean): void {
  app.setLoginItemSettings({
    openAtLogin: enabled,
    args: []
  });
}
