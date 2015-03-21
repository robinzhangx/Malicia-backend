import json
from pprint import pprint
from django.conf import settings
from django.test import TestCase, override_settings
import redis
from ft_accounts.models import User


class NotificationTest(TestCase):
    @override_settings(REDIS_DB=9)
    def setUp(self):
        r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
        r.flushdb()

    @override_settings(REDIS_DB=9)
    def test_notification_api(self):
        user = User()
        user.nickname = 'test'
        user.set_password('test_pass')
        user.is_superuser = True
        user.is_staff = True
        user.save()

        response = self.client.get('/api/notifications/?page=0')
        self.assertEqual(response.status_code, 403)

        self.client.login(nickname='test', password='test_pass')
        response = self.client.get('/api/notifications/?page=0')
        self.assertEqual(response.status_code, 200)

        for x in xrange(0, 100):
            response = self.client.post('/api/admin/notifications/', json.dumps({
                "user_id": user.id,
                "notification": {
                    "type": "short message",
                    "message": "Hello there {0}".format(x),
                    "from_id": 1,
                }
            }), content_type="application/json")
            self.assertEqual(response.status_code, 201)

        response = self.client.get('/api/notifications/?page=0')
        obj = json.loads(response.content)
        pprint(obj)
        self.assertEqual(len(obj['notifications']), 20)

        response = self.client.post('/api/notifications/100/', json.dumps({
            "read": True
        }), content_type="application/json")
        obj = json.loads(response.content)
        pprint(obj)
        self.assertIsNotNone(obj['read_at'])

        response = self.client.post('/api/notifications/100/', json.dumps({
            "read": False
        }), content_type="application/json")
        obj = json.loads(response.content)
        pprint(obj)
        self.assertIsNone(obj['read_at'])

