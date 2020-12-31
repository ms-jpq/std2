from datetime import datetime, timezone

utcnow = lambda: datetime.now(tz=timezone.utc)
