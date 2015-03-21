from fitting.mock_generator import MockGeneratorBase
from ft_accounts.models import User
from ft_social.models import Follow


class MockGenerator(MockGeneratorBase):
    @classmethod
    def generate_following(cls, clear=False, count=100):
        if clear:
            Follow.objects.all().delete()

        users = User.objects.all()

        for x in xrange(0, count):
            user1 = cls.pick_one(users)
            user2 = cls.pick_one(users)

            if user1.id != user2.id:
                try:
                    follow = Follow(left=user1, right=user2)
                    follow.save()
                except:
                    pass