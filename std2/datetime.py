from datetime import datetime, timezone

_MINUTE = 60
_HOUR = 60 * _MINUTE
_DAY = 24 * _HOUR
_WEEK = 7 * _DAY


def to_minutes(seconds: float) -> float:
    return seconds / _MINUTE


def to_hours(seconds: float) -> float:
    return seconds / _HOUR


def to_days(seconds: float) -> float:
    return seconds / _DAY


def to_weeks(seconds: float) -> float:
    return seconds / _WEEK


utcnow = lambda: datetime.now(tz=timezone.utc)


def utc_to_local(dt: datetime) -> datetime:
    return dt.replace(tzinfo=timezone.utc).astimezone(tz=None)
