# coding=utf-8
import json
from django.test import TestCase
from rest_framework import status
from ft_accounts.models import User
from ft_fitting.mock_generator import MockGenerator
from ft_fitting.models import Fitting, FittingForDiscover, Ingredient, LikeIngredient, LikeFitting


class FittingTest(TestCase):
    def test_fitting_count(self):
        user = User(nickname='test')
        user.save()
        f = Fitting()
        f.user = user
        f.save()

        response = self.client.get("/api/fittings/count/")
        self.assertEqual(response.status_code, 200)
        obj = json.loads(response.content)
        self.assertEqual(obj['count'], 1)

    def test_fitting_api(self):
        user = User(nickname='test')
        user.set_password('testpass')
        user.save()

        self.client.login(nickname='test', password='testpass')

        response = self.client.post("/api/fittings/", {
            "picture": "http://www.baidu.com",
            "title": "test",
        })
        print response.content
        self.assertEqual(response.status_code, 201)

    def test_ingredient_and_ask_api(self):
        user = User(nickname='test')
        user.set_password('testpass')
        user.save()

        fitting = Fitting()
        fitting.user = user
        fitting.bmi = user.bmi
        fitting.title = 'test title'
        fitting.picture = 'http://www.baidu.com'
        fitting.save()

        self.client.login(nickname='test', password='testpass')

        response = self.client.post("/api/ingredients/", {
            "part": u'上装',
            "size": "hahahh",
            "fitting": [fitting.id],
        })
        print response.content
        self.assertEqual(response.status_code, 201)

        response = self.client.post('/api/ingredients/1/asks/', {
            "content": u'哈哈',
            "ingredient": 1,
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.content)

        response = self.client.get('/api/ingredients/1/asks/')
        self.assertEqual(len(json.loads(response.content)), 1)

    def test_fitting_like_api(self):
        user = User(nickname='test')
        user.set_password('testpass')
        user.save()

        MockGenerator.create_fitting(user)

        self.client.login(nickname='test', password='testpass')

        response = self.client.post("/api/fittings/1/like/")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.content)
        self.assertTrue(LikeFitting.objects.filter(user_id=1, fitting_id=1).exists())

        response = self.client.post("/api/fittings/1/like/")
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        self.assertTrue(LikeFitting.objects.filter(user_id=1, fitting_id=1).exists())

        response = self.client.delete("/api/fittings/1/like/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, response.content)
        self.assertFalse(LikeFitting.objects.filter(user_id=1, fitting_id=1).exists())

    def test_ingredient_like_api(self):
        user = MockGenerator.create_user(nickname='test', password='test')
        MockGenerator.create_ingredient(user)
        self.client.login(nickname='test', password='test')

        response = self.client.post("/api/ingredients/1/like/")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.content)
        self.assertEqual(LikeIngredient.objects.all().count(), 1)

        response = self.client.post("/api/ingredients/1/like/")
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        self.assertEqual(LikeIngredient.objects.all().count(), 1)

        response = self.client.delete("/api/ingredients/1/like/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, response.content)
        self.assertEqual(LikeIngredient.objects.all().count(), 0)