from datetime import datetime
import json
from fitting.redis_store import redis_store


def create_notification(user_id, notification):
    """
    Notifications are store in redis in following format
    Each user have a notification sorted_set, with notification as score, the json body as value
    """
    notification_id = redis_store.incr('gbl.notification_id')
    notification.update({
        'read_at': None,
        'id': notification_id,
    })
    redis_store.zadd('user_notifications_{0}'.format(user_id), notification_id, json.dumps(notification))


def get_notifications(user_id, page=0, page_size=20):
    index = page * page_size
    return redis_store.zrevrange('user_notifications_{0}'.format(user_id), index, index + page_size - 1)


def get_notification(user_id, notification_id):
    key = 'user_notifications_{0}'.format(user_id)
    notifications = redis_store.zrangebyscore(key, notification_id, notification_id)

    if len(notifications) == 0:
        return None

    return json.loads(notifications[0])


def mark_notification(user_id, notification_id, read=True):
    notification = get_notification(user_id, notification_id)

    key = 'user_notifications_{0}'.format(user_id)
    redis_store.zremrangebyscore(key, notification_id, notification_id)

    if notification['read_at'] is None and read:
        notification['read_at'] = str(datetime.utcnow())
    elif notification['read_at'] is not None and not read:
        notification['read_at'] = None
    else:
        return notification

    redis_store.zadd(key, notification_id, json.dumps(notification))
    return notification
