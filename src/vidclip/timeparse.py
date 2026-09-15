def parse_timestamp(value: str) -> float:
    """Parse seconds, MM:SS, or HH:MM:SS into seconds."""
    text = value.strip()
    if not text:
        raise ValueError("timestamp is empty")

    if ":" not in text:
        try:
            seconds = float(text)
        except ValueError as exc:
            raise ValueError(f"invalid timestamp: {value!r}") from exc
        if seconds < 0:
            raise ValueError("timestamp cannot be negative")
        return seconds

    parts = text.split(":")
    if len(parts) not in (2, 3):
        raise ValueError(f"invalid timestamp: {value!r}")

    try:
        numbers = [float(part) for part in parts]
    except ValueError as exc:
        raise ValueError(f"invalid timestamp: {value!r}") from exc

    if any(n < 0 for n in numbers):
        raise ValueError("timestamp cannot be negative")

    if len(numbers) == 2:
        minutes, seconds = numbers
        return minutes * 60 + seconds

    hours, minutes, seconds = numbers
    return hours * 3600 + minutes * 60 + seconds
