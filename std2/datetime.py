from datetime import datetime, timezone

utcnow = lambda: datetime.now(tz=timezone.utc)


def utc_to_local(dt: datetime) -> datetime:
    return dt.replace(tzinfo=timezone.utc).astimezone(tz=None)

