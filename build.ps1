$ErrorActionPreference = "Stop"

if (-not (Get-Command pyinstaller -ErrorAction SilentlyContinue)) {
    Write-Host "PyInstaller not found. Install it with: pip install pyinstaller"
    exit 1
}

$iconJpg = Join-Path $PSScriptRoot "ico\myCat_ico.jpg"
$iconIco = Join-Path $PSScriptRoot "ico\myCat_ico.ico"

if (Test-Path $iconJpg) {
    @"
from pathlib import Path
from PIL import Image

src = Path(r"$iconJpg")
dst = Path(r"$iconIco")
image = Image.open(src).convert("RGBA")
image.save(dst, format="ICO", sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])
"@ | python -
}

if (Test-Path $iconIco) {
    pyinstaller --noconsole --onefile --name waterRing --icon $iconIco water_ring.py
} else {
    pyinstaller --noconsole --onefile --name waterRing water_ring.py
}
