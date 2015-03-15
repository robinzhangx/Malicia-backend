import random
from django.contrib.auth.models import User


class MockGeneratorBase(object):
    @classmethod
    def random_user(cls):
        users = User.objects.all()

        user_count = users.count()
        while True:
            index = random.randint(0, user_count - 1)
            yield users[index]

    @classmethod
    def pick_one(cls, items):
        if len(items) == 0:
            return None
        if len(items) == 1:
            return items[0]
        index = random.randint(0, len(items) - 1)
        return items[index]