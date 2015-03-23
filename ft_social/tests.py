import json
from pprint import pprint
from django.test import TestCase
from rest_framework import status
from fitting.redis_store import redis_store
from ft_accounts.models import User
from ft_notification.utils import get_notifications
from ft_social.models import Follow


class SocialTest(TestCase):
    def setUp(self):
        redis_store.flushdb()

        for i in xrange(0, 5):
            user = User()
            user.nickname = "user_%d" % i
            user.email = user.nickname + "@.test.com"
            user.set_password('testpass')
            user.save()

        users = User.objects.all()

        for i in xrange(0, 5):
            f = Follow()
            f.left = users[i]
            f.right = users[4 - i]
            f.save()

    def test_follow(self):
        self.assertEqual(redis_store.zcount('following_1', min=0, max=99999999999999999), 1)
        notifications = get_notifications(1)
        pprint(notifications)
        self.assertGreater(len(notifications), 0)
        self.assertEqual(json.loads(notifications[0]), {
            "follower": 5,
            "read_at": None,
            "type": "new_follower",
            "id": 5
        })

    def test_follow_api(self):
        u = User.objects.get(nickname='user_1')
        self.client.login(nickname='user_1', password='testpass')
        response = self.client.get('/api/social/followers/')
        self.assertEqual(response.status_code, 200)
        obj = json.loads(response.content)
        pprint(obj)
        self.assertEqual(len(obj), 1)

        response = self.client.get('/api/social/following/')
        self.assertEqual(response.status_code, 200)
        obj = json.loads(response.content)
        pprint(obj)
        self.assertEqual(len(obj), 1)

        response = self.client.post('/api/social/following/', {
            'user': 3
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post('/api/social/following/', {
            'user': u.id
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post('/api/social/following/', {
            'user': 199999999999
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Follow again, you get a 200
        response = self.client.post('/api/social/following/', {
            'user': 3
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check following list, we got 2 followers
        response = self.client.get('/api/social/following/')
        self.assertEqual(response.status_code, 200)
        obj = json.loads(response.content)
        pprint(obj)
        self.assertEqual(len(obj), 2)

        response = self.client.get('/api/social/following/3/')
        self.assertEqual(response.status_code, 200)
        obj = json.loads(response.content)
        pprint(obj)
        self.assertTrue(obj['following'])

