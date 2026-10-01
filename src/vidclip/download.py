from __future__ import annotations

from pathlib import Path

import yt_dlp

QUALITIES = (1080, 720, 480, 360)


def parse_quality(value: str) -> int:
    text = value.strip().lower().rstrip("p")
    allowed = ", ".join(str(item) for item in QUALITIES)
    try:
        height = int(text)
    except ValueError as exc:
        raise ValueError(f"quality must be {allowed}") from exc
    if height not in QUALITIES:
        raise ValueError(f"quality must be {allowed}")
    return height


def format_selector(height: int) -> str:
    return (
        f"bestvideo[height={height}][ext=mp4]+bestaudio[ext=m4a]/"
        f"bestvideo[height={height}]+bestaudio/"
        f"bestvideo[height<={height}]+bestaudio/"
        f"best[height<={height}]"
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
    quality: int = 1080,
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
        "format": format_selector(quality),
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
