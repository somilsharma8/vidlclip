from __future__ import annotations

import os
import platform
import shutil
import sys
import urllib.request
import zipfile
from pathlib import Path

import imageio_ffmpeg

JS_RUNTIME_NAMES = ("deno", "node", "bun", "quickjs")
DENO_RELEASE = "https://github.com/denoland/deno/releases/latest/download"


def app_dir() -> Path:
    if os.name == "nt":
        root = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
    else:
        root = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))
    return root / "vidclip"


def bundled_bin_dir() -> Path:
    return app_dir() / "bin"


def bundled_deno_path() -> Path:
    name = "deno.exe" if os.name == "nt" else "deno"
    return bundled_bin_dir() / name


def ffmpeg_path() -> str:
    found = shutil.which("ffmpeg")
    if found:
        return found
    return imageio_ffmpeg.get_ffmpeg_exe()


def _deno_zip_name() -> str:
    system = platform.system()
    machine = platform.machine().lower()
    arm = machine in {"arm64", "aarch64"}
    if system == "Windows":
        arch = "aarch64" if arm else "x86_64"
        return f"deno-{arch}-pc-windows-msvc.zip"
    if system == "Darwin":
        arch = "aarch64" if arm else "x86_64"
        return f"deno-{arch}-apple-darwin.zip"
    arch = "aarch64" if arm else "x86_64"
    return f"deno-{arch}-unknown-linux-gnu.zip"


def install_deno() -> Path:
    dest = bundled_deno_path()
    if dest.exists():
        return dest

    bundled_bin_dir().mkdir(parents=True, exist_ok=True)
    url = f"{DENO_RELEASE}/{_deno_zip_name()}"
    archive = bundled_bin_dir() / "deno.zip"
    print(f"Downloading Deno (needed for YouTube) from {url} ...", file=sys.stderr)
    request = urllib.request.Request(url, headers={"User-Agent": "vidclip"})
    with urllib.request.urlopen(request) as response, archive.open("wb") as handle:
        shutil.copyfileobj(response, handle)

    with zipfile.ZipFile(archive) as zipped:
        zipped.extractall(bundled_bin_dir())
    archive.unlink(missing_ok=True)

    if os.name != "nt":
        dest.chmod(dest.stat().st_mode | 0o111)
    if not dest.exists():
        raise RuntimeError("Deno downloaded, but the executable was not found in the zip.")
    print(f"Installed Deno to {dest}", file=sys.stderr)
    return dest


def js_runtimes() -> dict[str, dict[str, str]]:
    runtimes: dict[str, dict[str, str]] = {}
    bundled = bundled_deno_path()
    if bundled.exists():
        runtimes["deno"] = {"path": str(bundled)}
    for name in JS_RUNTIME_NAMES:
        found = shutil.which(name)
        if found:
            runtimes[name] = {"path": found}
    return runtimes


def require_tools() -> tuple[str, dict[str, dict[str, str]]]:
    ffmpeg = ffmpeg_path()
    if not Path(ffmpeg).exists():
        raise RuntimeError(
            "ffmpeg is missing. Reinstall vidclip (it should bundle ffmpeg), "
            "or install ffmpeg and add it to PATH."
        )

    runtimes = js_runtimes()
    if not runtimes:
        install_deno()
        runtimes = js_runtimes()
    if not runtimes:
        raise RuntimeError(
            "YouTube downloads need a JavaScript runtime. vidclip tried to install Deno "
            "automatically and failed. Install Node.js 20+ from https://nodejs.org "
            "or Deno, then run: vidclip doctor"
        )
    return ffmpeg, runtimes
