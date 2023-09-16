from django.utils import timezone
from django_redis import get_redis_connection


CONNECTION = get_redis_connection("streams")
STREAM_LENGTH = 128


def add_online_flag(username):
    """
    Create record of online
    activity of users
    """

    key = f"ONLINE:{username.upper()}"
    timestamp = timezone.now()
    data = {"timestamp": f"{timestamp}"}

    return CONNECTION.xadd(key, data, maxlen=STREAM_LENGTH)


def get_online_flag(username):
    """
    Get last activity record
    """
    key = f"ONLINE:{username.upper()}"

    return CONNECTION.xrevrange(key, max="+", min="-", count=1)
