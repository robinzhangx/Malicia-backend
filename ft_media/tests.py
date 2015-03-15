from django.contrib.auth.models import User
from django.test import TestCase


class UploadAPITest(TestCase):
    def test_image_upload(self):
        u = User(username="test")
        u.set_password("testpass")
        u.save()

        self.client.login(username='test', password='testpass')

        with open('static/images/background.jpg') as fp:
            response = self.client.put('/api/images/test.jpg', fp.read())
            self.assertEqual(response.status_code, 204)
            print response.data
