from django.test import TestCase
from ft_accounts.models import User


class UploadAPITest(TestCase):
    def test_image_upload(self):
        u = User(nickname="test")
        u.set_password("testpass")
        u.save()

        self.client.login(username='test', password='testpass')

        with open('static/images/background.jpg') as fp:
            response = self.client.put('/api/images/test', fp.read())
            self.assertEqual(response.status_code, 200)
            print response.data

        with open('static/images/background.jpg') as fp:
            response = self.client.put('/api/images/test', fp.read())
            self.assertEqual(response.status_code, 200)
            print response.data
