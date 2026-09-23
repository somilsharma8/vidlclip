from __future__ import annotations

import argparse
import importlib.metadata
import shutil
import subprocess
import sys
from pathlib import Path

import yt_dlp

from vidclip import __version__
from vidclip.download import download_clip, parse_quality
from vidclip.runtime import bundled_deno_path, ffmpeg_path, js_runtimes, require_tools
from vidclip.timeparse import parse_timestamp

EXAMPLES = """
examples:
  vidclip
  vidclip "https://www.youtube.com/watch?v=VIDEO_ID"
  vidclip "https://www.youtube.com/watch?v=VIDEO_ID" --start 1:20 --end 2:05
  vidclip "https://www.youtube.com/watch?v=VIDEO_ID" --quality 720
  vidclip "https://www.youtube.com/watch?v=VIDEO_ID" -q 480
  vidclip doctor
  vidclip update
"""


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="vidclip",
        description=(
            "Download a YouTube video or a time-range clip. Choose 1080p, 720p, "
            "or 480p (falls back to a lower size if the chosen one is missing). "
            "Run with no arguments for an interactive prompt."
        ),
        epilog=EXAMPLES,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "url",
        nargs="?",
        help="YouTube video URL (optional; you will be prompted if omitted)",
    )
    parser.add_argument(
        "-s",
        "--start",
        help="Clip start time: seconds, MM:SS, or HH:MM:SS",
    )
    parser.add_argument(
        "-e",
        "--end",
        help="Clip end time: seconds, MM:SS, or HH:MM:SS",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Output filename (extension is usually .mp4)",
    )
    parser.add_argument(
        "-d",
        "--out-dir",
        default=".",
        help="Directory to write the file into (default: current directory)",
    )
    parser.add_argument(
        "-q",
        "--quality",
        default="1080",
        help="Resolution: 1080, 720, or 480 (default: 1080)",
    )
    return parser


def _prompt(label: str) -> str:
    try:
        return input(label).strip()
    except EOFError:
        return ""


def interactive_download() -> tuple[str, str | None, str | None, str | None, str]:
    print("vidclip — paste a YouTube link. Leave clip times blank to download the full video.")
    url = _prompt("YouTube URL: ")
    if not url:
        raise SystemExit("error: a YouTube URL is required")
    start = _prompt("Start time (e.g. 1:20, blank = beginning): ") or None
    end = _prompt("End time (e.g. 2:05, blank = end): ") or None
    quality = _prompt("Quality: 1080, 720, or 480 (blank = 1080): ") or "1080"
    output = _prompt("Save as (blank = video title): ") or None
    return url, start, end, output, quality


def run_doctor() -> int:
    print(f"vidclip {__version__}")
    print(f"Python  {sys.version.split()[0]}  ({sys.executable})")

    try:
        ytdlp_version = importlib.metadata.version("yt-dlp")
    except importlib.metadata.PackageNotFoundError:
        ytdlp_version = getattr(yt_dlp, "version", None)
        ytdlp_version = getattr(ytdlp_version, "__version__", "unknown")
    print(f"yt-dlp  {ytdlp_version}")

    ffmpeg = ffmpeg_path()
    print(f"ffmpeg  {ffmpeg}" if Path(ffmpeg).exists() else "ffmpeg  MISSING")

    runtimes = js_runtimes()
    if runtimes:
        for name, meta in runtimes.items():
            print(f"js      {name}  {meta['path']}")
    else:
        bundled = bundled_deno_path()
        print(f"js      none on PATH (will auto-install Deno to {bundled.parent})")

    command = shutil.which("vidclip")
    print(f"command {command or 'vidclip is not on PATH in this terminal'}")
    return 0 if Path(ffmpeg).exists() else 1


def run_update() -> int:
    print("Updating yt-dlp (YouTube support breaks if this gets stale)...")
    return subprocess.call(
        [sys.executable, "-m", "pip", "install", "-U", "yt-dlp[default]"]
    )


def run_download(args: argparse.Namespace) -> int:
    url = args.url
    start_text = args.start
    end_text = args.end
    output_text = args.output
    quality_text = args.quality
    if not url:
        url, start_text, end_text, output_text, quality_text = interactive_download()

    start = parse_timestamp(start_text) if start_text else None
    end = parse_timestamp(end_text) if end_text else None
    quality = parse_quality(quality_text)
    ffmpeg, runtimes = require_tools()
    saved = download_clip(
        url,
        start=start,
        end=end,
        output=Path(output_text) if output_text else None,
        out_dir=Path(args.out_dir),
        ffmpeg=ffmpeg,
        js_runtimes=runtimes,
        quality=quality,
    )
    if saved:
        print(f"Saved: {saved.resolve()}")
    return 0


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv and argv[0] == "doctor":
        return run_doctor()
    if argv and argv[0] == "update":
        return run_update()

    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return run_download(args)
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        print("If YouTube fails, run: vidclip update   then   vidclip doctor", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
