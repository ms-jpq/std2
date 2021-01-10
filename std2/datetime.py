from datetime import datetime, timezone

utcnow = lambda: datetime.now(tz=timezone.utc)

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
