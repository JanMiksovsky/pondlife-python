import re
from datetime import datetime, timedelta, timezone


def parse_date(text):
    """Parse a YYYY-MM-DD date from the start of the text and return a datetime in US Eastern Time (UTC-5)."""
    match = re.match(r'^(?P<date>\d{4}-\d{2}-\d{2})', text)
    if not match:
        return None
    date_str = match.group('date')
    # Noon in US Eastern Time (UTC-5)
    dt = datetime.strptime(date_str + ' 12:00', '%Y-%m-%d %H:%M')
    eastern = timezone(timedelta(hours=-5))
    return dt.replace(tzinfo=eastern)
