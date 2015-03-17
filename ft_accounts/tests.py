# coding=utf-8
import json
from pprint import pprint
from django.contrib.auth import authenticate
from ft_accounts.models import User
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

        pprint(response.content)

        self.assertEqual(response.status_code, 409)

    def test_user_register_dup_email(self):
        response = self.client.get('/api/accounts/register/')
        self.assertEqual(response.status_code, 405)

        response = self.client.post("/api/accounts/register/", {
            'nickname': 'nickname',
            'email': 'test@test.com',
            'password': 'testpass'
        })

        self.assertEqual(response.status_code, 201)

        response = self.client.post("/api/accounts/register/", {
            'nickname': 'nick',
            'email': 'test@test.com',
            'password': 'testpass'
        })

        pprint(response.content)

        self.assertEqual(response.status_code, 409)

    def test_user_login_fail(self):
        response = self.client.post("/api/accounts/register/", {
            'nickname': 'nickname',
            'email': 'test@test.com',
            'password': 'testpass'
        })

        response = self.client.post("/api/accounts/login/", {
            'identifier': 'nickname',
            'password': 'testpassss'
        })
        self.assertEqual(response.status_code, 400)
        obj = json.loads(response.content)
        self.assertEqual(obj["code"], 4002)

        response = self.client.post("/api/accounts/login/", {
            'password': 'testpass'
        })
        self.assertEqual(response.status_code, 400)
        obj = json.loads(response.content)
        pprint(obj)
        self.assertEqual(obj["code"], 40040)

    def test_user_nickname_unicode(self):
        response = self.client.post("/api/accounts/register/", {
            'nickname': u'  哈哈哈  ',
            'email': 'test@test.com',
            'password': 'testpass'
        })

        self.assertEqual(response.status_code, 201)
        user = User.objects.get(id=1)
        self.assertEqual(user.nickname, u'哈哈哈')

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
        user = User(nickname="test", email="test@test.com")
        user.set_password("hahahah")
        user.save()
        user = authenticate(nickname="test", password="hahahah")
        self.assertIsNotNone(user)

        user = authenticate(email="test@test.com", password="hahahah")
        self.assertIsNotNone(user)

    def test_user_login_nickname(self):
        self.client.post("/api/accounts/register/", {
            'nickname': u'  哈哈哈  ',
            'email': 'test@test.com',
            'password': 'testpass'
        })

        res = self.client.post("/api/accounts/login/", {
            'identifier': u'哈哈哈',
            'password': 'testpass'
        })

        pprint(res.content)
        self.assertEqual(res.status_code, 201)

    def test_user_login_email(self):
        self.client.post("/api/accounts/register/", {
            'nickname': u'  哈哈哈  ',
            'email': 'test@test.com',
            'password': 'testpass'
        })

        res = self.client.post("/api/accounts/login/", {
            'identifier': 'test@test.com',
            'password': 'testpass'
        })

        pprint(res.content)
        self.assertEqual(res.status_code, 201)

    def test_weixin_bind(self):
        response = self.client.post('/api/accounts/bind/weixin/', {
            "access_token": "OezXcEiiBSKSxW0eoylIeMYxHx-1KFpzC8sjKIw3QJKJrOvfUsHqXnoEHwaT86uB4j6sSUOB7Ja0RguxeocwVo9WE27zgQIV4RdzeahoPl7BCZSM51qPLqoW8b69N2xy9NYDB0Tac0HG6saA_nlx_w",
            "expires_in": 7200,
            "openid": "oMA2BuD8GVqc27rdyFC5cahrfvDA",
            "refresh_token": "OezXcEiiBSKSxW0eoylIeMYxHx-1KFpzC8sjKIw3QJKJrOvfUsHqXnoEHwaT86uBw2VpHTkdh6N9mnzGrwIPvC5X_9KvbIioysyMEMApY0lHqel35E3I9SgyKO4RMtJ4QE13yxwVpRA_kJYjVm91jw",
            "scope": "snsapi_userinfo",
            "unionid": "o-p4Ss4dS3Z8hE33nL0YPP4yeZw4",
            "city": "Haidian",
            "country": "CN",
            "headimgurl": "http://wx.qlogo.cn/mmopen/ajNVdqHZLLCMIkG3POj0tPzxGiaGvpk9GRGZN92NCP0TsTCib6VGCDe4ichSLOheHXbYZAdic35lTKvUmaYCa4G6nA/0",
            "language": "en",
            "nickname": "Robin",
            "province": "Beijing",
            "sex": 1,
        })

        self.assertEqual(response.status_code, 201)
        pprint(response.content)
        obj = json.loads(response.content)

        self.assertIsNotNone(obj.get('token', None))
        token = obj['token']

        response = self.client.post('/api/accounts/bind/weixin/', {
            "access_token": "OezXcEiiBSKSxW0eoylIeMYxHx-1KFpzC8sjKIw3QJKJrOvfUsHqXnoEHwaT86uB4j6sSUOB7Ja0RguxeocwVo9WE27zgQIV4RdzeahoPl7BCZSM51qPLqoW8b69N2xy9NYDB0Tac0HG6saA_nlx_w",
            "expires_in": 7200,
            "openid": "oMA2BuD8GVqc27rdyFC5cahrfvDA",
            "refresh_token": "OezXcEiiBSKSxW0eoylIeMYxHx-1KFpzC8sjKIw3QJKJrOvfUsHqXnoEHwaT86uBw2VpHTkdh6N9mnzGrwIPvC5X_9KvbIioysyMEMApY0lHqel35E3I9SgyKO4RMtJ4QE13yxwVpRA_kJYjVm91jw",
            "scope": "snsapi_userinfo",
            "unionid": "o-p4Ss4dS3Z8hE33nL0YPP4yeZw4",
            "city": "Haidian",
            "country": "CN",
            "headimgurl": "http://wx.qlogo.cn/mmopen/ajNVdqHZLLCMIkG3POj0tPzxGiaGvpk9GRGZN92NCP0TsTCib6VGCDe4ichSLOheHXbYZAdic35lTKvUmaYCa4G6nA/0",
            "language": "en",
            "nickname": "Robin",
            "province": "Beijing",
            "sex": 1,
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['token'], token)
