/// <reference types="vite/client" />

interface WaterRingApi {
  getSettings(): Promise<{
    intervalMinutes: number;
    snoozeMinutes: number;
    reminderSeconds: number;
    launchMinimized: boolean;
    autoStart: boolean;
  }>;
  setSettings(next: Partial<{
    intervalMinutes: number;
    snoozeMinutes: number;
    reminderSeconds: number;
    launchMinimized: boolean;
    autoStart: boolean;
  }>): Promise<unknown>;
  confirmWater(): Promise<number>;
  snooze(): Promise<number>;
  getNextReminderAt(): Promise<number>;
  onReminderShow(callback: () => void): () => void;
}

interface Window {
  waterRing: WaterRingApi;
}
