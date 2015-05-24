# coding=utf-8
import json
from django.test import TestCase
from rest_framework import status
from ft_accounts.models import User
from ft_fitting.mock_generator import MockGenerator
from ft_fitting.models import Fitting, FittingForDiscover, Ingredient, LikeIngredient, LikeFitting, Ask


class FittingTest(TestCase):
    def fitting_obj(self, fitting_id):
        response = self.client.get('/api/fittings/{0}/'.format(fitting_id))
        return json.loads(response.content)

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
        user.bmi = 27
        user.save()

        self.client.login(nickname='test', password='testpass')

        response = self.client.post("/api/fittings/", {
            "picture": "http://www.baidu.com",
            "title": "test",
        })
        self.assertEqual(response.status_code, 201)
        obj = json.loads(response.content)
        self.assertEqual(obj['like_count'], 0)

        # Create several fittings with different bmi
        bmis = [21, 23, 28, 25]
        for bmi in bmis:
            fitting = Fitting()
            fitting.bmi = bmi
            fitting.user = user
            fitting.save()

        response = self.client.get("/api/fittings/")
        obj = json.loads(response.content)
        print response.content
        self.assertEqual(obj[0]['bmi'], 27)
        self.assertEqual(obj[1]['bmi'], 28)

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
        self.assertEqual(response.status_code, 201)

        response = self.client.post('/api/ingredients/1/asks/', {
            "content": u'哈哈',
            "ingredient": 1,
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.content)
        self.assertEqual(Ask.objects.all().count(), 1)

        response = self.client.get('/api/ingredients/1/asks/')
        print response.content
        self.assertEqual(len(json.loads(response.content)), 1)

    def test_ingredient_create_under_fitting(self):
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

        response = self.client.post("/api/fittings/%d/ingredients/" % fitting.id, {
            "part": u'上装',
            "size": "hahahh",
        })
        print response.content
        self.assertEqual(response.status_code, 201)

    def test_fitting_like_api(self):
        user = User(nickname='test')
        user.set_password('testpass')
        user.save()

        fitting = MockGenerator.create_fitting(user)

        self.client.login(nickname='test', password='testpass')

        response = self.client.post("/api/fittings/1/like/")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.content)
        self.assertTrue(LikeFitting.objects.filter(user_id=1, fitting_id=1).exists())

        fitting = self.fitting_obj(fitting.id)
        self.assertEqual(fitting['like_count'], 1)

        response = self.client.post("/api/fittings/1/like/")
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        self.assertTrue(LikeFitting.objects.filter(user_id=1, fitting_id=1).exists())

        fitting = self.fitting_obj(fitting['id'])
        self.assertEqual(fitting['like_count'], 1)

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