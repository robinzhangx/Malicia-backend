import json
from django.test import TestCase
from ft_accounts.models import User
from ft_fitting.models import Fitting


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