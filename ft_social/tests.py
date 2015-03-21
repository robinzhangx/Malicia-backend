import json
from pprint import pprint
from django.test import TestCase

# Create your tests here.
from fitting.redis_store import redis_store
from ft_accounts.models import User
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

    def test_follow_api(self):
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

