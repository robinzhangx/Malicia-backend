import json
from django.test import TestCase
from ft_accounts.models import User
from ft_fitting.models import Fitting, FittingForDiscover


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

    def test_fitting_for_discover(self):
        user = User(nickname='test')
        user.save()

        f = Fitting()
        f.user = user
        f.save()

        discover = FittingForDiscover()
        discover.fitting = f
        discover.save()

        response = self.client.get("/api/fittings/discover/")
        self.assertEqual(response.status_code, 200)
        obj = json.loads(response.content)
        self.assertEqual(obj['discover_id'], 1)

        response = self.client.get("/api/fittings/discover/?last_discover_id=1")
        self.assertEqual(response.status_code, 400)
        obj = json.loads(response.content)
        self.assertEqual(obj['code'], 4000)