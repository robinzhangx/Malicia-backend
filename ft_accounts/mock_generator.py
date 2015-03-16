from ft_accounts.models import User
from fitting.mock_generator import MockGeneratorBase


class MockGenerator(MockGeneratorBase):
    @classmethod
    def generate_user(cls, clear=False, count=100):
        if clear:
            # Should not clear superuser
            User.objects.filter(is_superuser=False).delete()

        for x in xrange(0, count):
            u = User(username="user_%d" % x)
            u.set_password("testpass")
            u.email = u.username + "@fitting.com"
            u.save()