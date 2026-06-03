import Store from "electron-store";
import { DEFAULT_SETTINGS, type Settings } from "./config";

type Schema = {
  settings: Settings;
  nextReminderAt: number;
};

const store = new Store<Schema>({
  name: "waterring",
  defaults: {
    settings: DEFAULT_SETTINGS,
    nextReminderAt: Date.now() + DEFAULT_SETTINGS.intervalMinutes * 60_000
  }
});

export const settingsStore = {
  getSettings(): Settings {
    return store.get("settings");
  },
  setSettings(next: Partial<Settings>): Settings {
    const current = store.get("settings");
    const merged = { ...current, ...next };
    store.set("settings", merged);
    return merged;
  },
  getNextReminderAt(): number {
    return store.get("nextReminderAt");
  },
  setNextReminderAt(value: number): void {
    store.set("nextReminderAt", value);
  }
};
