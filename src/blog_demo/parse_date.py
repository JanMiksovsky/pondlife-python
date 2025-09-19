import re
from datetime import datetime, timedelta, timezone


def parse_date(s: str) -> datetime | None:
    """
    Parse a YYYY-MM-DD date from the start of the text and return a datetime in
    US Eastern Time (UTC-5).
    """
    match = re.match(r'^(?P<date>\d{4}-\d{2}-\d{2})', s)
    if not match:
        return None
    date_str = match.group('date')
    dt = datetime.strptime(date_str + ' 12:00', '%Y-%m-%d %H:%M')
    eastern = timezone(timedelta(hours=-5))  # UTC-5, adjust as desired
    return dt.replace(tzinfo=eastern)
