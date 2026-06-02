# Running waterRing

This project is a Windows desktop water-reminder assistant built with Python and Tkinter.

## Requirements

- Windows 10 or Windows 11
- Python 3.10 or newer
- Tkinter available in your Python installation

## Clone and run

```bash
git clone <your-repo-url>
cd waterRing
python water_ring.py
```

## Project entry points

- `water_ring.py` is the recommended launch file
- `water_ring_app/main.py` contains the application entry

## What it does

- Shows a cute cat reminder window at scheduled intervals
- Can stay minimized in the tray
- Supports settings for reminder interval, snooze, popup duration, cat style, and startup behavior
- Supports Windows startup registration

## Notes

- Tray and startup features are Windows-specific
- No third-party dependencies are required
- If the app appears to do nothing on launch, check whether it started minimized to tray

## Packaging

If you want to build an executable later, keep `water_ring.py` as the entry point and package the project from the repository root.
