from __future__ import annotations

from pathlib import Path

import yt_dlp

# Prefer 1080p MP4 when possible, then 720p, then the best video at or below 1080p.
FORMAT = (
    "bestvideo[height=1080][ext=mp4]+bestaudio[ext=m4a]/"
    "bestvideo[height=1080]+bestaudio/"
    "bestvideo[height=720][ext=mp4]+bestaudio[ext=m4a]/"
    "bestvideo[height=720]+bestaudio/"
    "bestvideo[height<=1080]+bestaudio/"
    "best[height<=1080]"
)


def download_clip(
    url: str,
    *,
    start: float | None,
    end: float | None,
    output: Path | None,
    out_dir: Path,
    ffmpeg: str,
    js_runtimes: dict[str, dict[str, str]],
) -> Path | None:
    if start is not None and end is not None and end <= start:
        raise ValueError("end time must be after start time")

    out_dir.mkdir(parents=True, exist_ok=True)

    if output is not None:
        output_path = output if output.is_absolute() else out_dir / output
        output_path.parent.mkdir(parents=True, exist_ok=True)
        outtmpl = str(output_path.with_suffix(".%(ext)s"))
    else:
        outtmpl = str(out_dir / "%(title)s.%(ext)s")

    opts: dict = {
        "format": FORMAT,
        "merge_output_format": "mp4",
        "outtmpl": outtmpl,
        "noplaylist": True,
        "ffmpeg_location": ffmpeg,
        "js_runtimes": js_runtimes,
        "quiet": False,
        "noprogress": False,
    }

    if start is not None or end is not None:
        clip_start = 0.0 if start is None else start

        def download_ranges(info_dict, _ydl):
            duration = info_dict.get("duration")
            clip_end = end if end is not None else duration
            if clip_end is None:
                return [{"start_time": clip_start}]
            return [{"start_time": clip_start, "end_time": float(clip_end)}]

        opts["download_ranges"] = download_ranges
        opts["force_keyframes_at_cuts"] = True

    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=True)

    return _saved_path(info)


def _saved_path(info: dict | None) -> Path | None:
    if not info:
        return None
    downloads = info.get("requested_downloads") or []
    for item in downloads:
        for key in ("filepath", "filename"):
            value = item.get(key)
            if value:
                return Path(value)
    filename = info.get("filename") or info.get("_filename")
    return Path(filename) if filename else None
