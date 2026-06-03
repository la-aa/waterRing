export type Settings = {
  intervalMinutes: number;
  snoozeMinutes: number;
  reminderSeconds: number;
  launchMinimized: boolean;
  autoStart: boolean;
};

export const DEFAULT_SETTINGS: Settings = {
  intervalMinutes: 60,
  snoozeMinutes: 15,
  reminderSeconds: 10,
  launchMinimized: true,
  autoStart: false
};
