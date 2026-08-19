from datetime import datetime, timezone
from zoneinfo import ZoneInfo

def format_scan_time(scan_time: str) -> str:
    dt = datetime.fromisoformat(
        scan_time.replace("Z", "+00:00")
    )

    dt = dt.astimezone(ZoneInfo("Asia/Kolkata"))

    return dt.strftime("%d %b %Y · %I:%M %p")

def format_elapsed_time(scan_time: str) -> str:
    scan_datetime = datetime.fromisoformat(
        scan_time.replace("Z", "+00:00")
    )

    elapsed = datetime.now(timezone.utc) - scan_datetime

    seconds = int(elapsed.total_seconds())

    if seconds < 60:
        return "Just now"

    minutes = seconds // 60

    if minutes < 60:
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"

    hours = minutes // 60

    if hours < 24:
        return f"{hours} hour{'s' if hours != 1 else ''} ago"

    days = hours // 24

    if days < 7:
        return f"{days} day{'s' if days != 1 else ''} ago"

    weeks = days // 7

    if weeks < 4:
        return f"{weeks} week{'s' if weeks != 1 else ''} ago"

    months = days // 30

    return f"{months} month{'s' if months != 1 else ''} ago"
