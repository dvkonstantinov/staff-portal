from datetime import datetime, timedelta, timezone


def get_last_month_users(users):
    now = datetime.now(timezone.utc)
    diff = now - timedelta(days=30)

    users.filter(date_joined__gt=diff)
    return users


def get_last_month_objects(objs):
    now = datetime.now(timezone.utc)
    diff = now - timedelta(days=30)

    objs.filter(created_at__gt=diff)
    return objs
