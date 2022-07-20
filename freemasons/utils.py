import datetime
import django

# 12 hours
SECONDS_BETWEEN_SYNC = 60 * 60 * 12

def needs_sync(last_sync_at):
    if not last_sync_at:
        return True

    return last_sync_at - datetime.timedelta(seconds=SECONDS_BETWEEN_SYNC) > django.utils.timezone.now()
