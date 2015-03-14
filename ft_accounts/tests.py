# coding=utf-8
import json
from pprint import pprint
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.test import TestCase


class UserTest(TestCase):
    def test_user_register(self):
        response = self.client.get('/api/accounts/register/')
        self.assertEqual(response.status_code, 405)

        response = self.client.post("/api/accounts/register/", {
            'nickname': 'nickname',
            'email': 'test@test.com',
            'password': 'testpass'
        })

        self.assertEqual(response.status_code, 201)

        response = self.client.post("/api/accounts/register/", {
            'nickname': 'nickname',
            'email': 'test@test.com',
            'password': 'testpass'
        })

        self.assertEqual(response.status_code, 409)

    def test_user_nickname_unicode(self):
        response = self.client.post("/api/accounts/register/", {
            'nickname': u'  哈哈哈  ',
            'email': 'test@test.com',
            'password': 'testpass'
        })

        self.assertEqual(response.status_code, 201)
        user = User.objects.get(id=1)
        self.assertEqual(user.username, u'哈哈哈')

    def test_user_logout(self):
        response = self.client.post("/api/accounts/register/", {
            'nickname': u'  哈哈哈  ',
            'email': 'test@test.com',
            'password': 'testpass'
        })

        res = json.loads(response.content)
        response = self.client.post("/api/accounts/logout", **{
            "HTTP_AUTHORIZATION": "Token %s" % res['token']
        })

        self.assertEqual(response.status_code, 200)

    def test_auth_backend(self):
        user = User(username="test", email="test@test.com")
        user.set_password("hahahah")
        user.save()
        user = authenticate(nickname="test", password="hahahah")
        self.assertIsNotNone(user)

        user = authenticate(email="test@test.com", password="hahahah")
        self.assertIsNotNone(user)

    def test_user_login(self):
        self.client.post("/api/accounts/register/", {
            'nickname': u'  哈哈哈  ',
            'email': 'test@test.com',
            'password': 'testpass'
        })

        res = self.client.post("/api/accounts/login/", {
            'nickname': u'哈哈哈',
            'password': 'testpass'
        })

        pprint(res.content)
        self.assertEqual(res.status_code, 201)


