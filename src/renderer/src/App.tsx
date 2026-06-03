import { useEffect, useMemo, useState } from "react";

type Settings = {
  intervalMinutes: number;
  snoozeMinutes: number;
  reminderSeconds: number;
  launchMinimized: boolean;
  autoStart: boolean;
};

const defaultSettings: Settings = {
  intervalMinutes: 60,
  snoozeMinutes: 15,
  reminderSeconds: 10,
  launchMinimized: true,
  autoStart: false
};

export default function App() {
  const [settings, setSettings] = useState<Settings>(defaultSettings);
  const [nextReminderAt, setNextReminderAt] = useState<number>(Date.now() + 60 * 60 * 1000);
  const [message, setMessage] = useState("喵~ 记得喝水哦");
  const [bridgeReady, setBridgeReady] = useState(false);
  const api = window.waterRing;

  useEffect(() => {
    if (!api) {
      setMessage("渲染层已启动，但桥接接口没有加载成功。");
      return;
    }

    setBridgeReady(true);
    api.getSettings().then(setSettings).catch(() => setMessage("读取设置失败"));
    api.getNextReminderAt().then(setNextReminderAt).catch(() => {});
    return api.onReminderShow(() => {
      setMessage("喵！该喝水啦。");
    });
  }, []);

  const nextText = useMemo(() => {
    const diff = Math.max(0, nextReminderAt - Date.now());
    const minutes = Math.ceil(diff / 60000);
    return `${minutes} 分钟后提醒`;
  }, [nextReminderAt]);

  async function save(partial: Partial<Settings>) {
    if (!api) return;
    const next = { ...settings, ...partial };
    setSettings(next);
    await api.setSettings(next);
  }

  async function confirm() {
    if (!api) return;
    const next = await api.confirmWater();
    setNextReminderAt(next);
    setMessage("好，记下啦。下一次再来叫你。");
  }

  async function snooze() {
    if (!api) return;
    const next = await api.snooze();
    setNextReminderAt(next);
    setMessage("那我先安静一会儿。");
  }

  return (
    <main className="app">
      <section className="hero">
        <div className="pet-shell">
          <div className="pet-face">
            <div className="ear left" />
            <div className="ear right" />
            <div className="eye left" />
            <div className="eye right" />
            <div className="nose" />
            <div className="cheek left" />
            <div className="cheek right" />
          </div>
        </div>
        <div className="hero-copy">
          <h1>waterRing</h1>
          <p>{message}</p>
          <div className="status">{nextText}</div>
          {!bridgeReady && <div className="status">Waiting for bridge...</div>}
        </div>
      </section>

      <section className="panel">
        <label>
          提醒间隔
          <input type="number" min={10} max={240} value={settings.intervalMinutes} onChange={(e) => save({ intervalMinutes: Number(e.target.value) })} />
        </label>
        <label>
          稍后提醒
          <input type="number" min={1} max={120} value={settings.snoozeMinutes} onChange={(e) => save({ snoozeMinutes: Number(e.target.value) })} />
        </label>
        <label>
          弹出停留
          <input type="number" min={3} max={60} value={settings.reminderSeconds} onChange={(e) => save({ reminderSeconds: Number(e.target.value) })} />
        </label>
        <label className="row">
          <input type="checkbox" checked={settings.autoStart} onChange={(e) => save({ autoStart: e.target.checked })} />
          开机自启
        </label>
        <label className="row">
          <input type="checkbox" checked={settings.launchMinimized} onChange={(e) => save({ launchMinimized: e.target.checked })} />
          启动后最小化到托盘
        </label>
      </section>

      <section className="actions">
        <button onClick={confirm}>我喝了</button>
        <button className="secondary" onClick={snooze}>稍后提醒</button>
      </section>
    </main>
  );
}
