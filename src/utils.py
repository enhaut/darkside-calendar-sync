EVENTID_CALSYNC_PREFIX = "CALSYNC"

def get_event_id(training_id: int, date: str):
    escaped_date = date.replace(':', '')
    return f"{EVENTID_CALSYNC_PREFIX}{training_id}-{escaped_date}"

