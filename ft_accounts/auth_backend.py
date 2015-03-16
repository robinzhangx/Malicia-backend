from ft_accounts.models import User


class AuthBackend(object):
    def authenticate(self, password, nickname=None, email=None):
        password = password

        if nickname is not None:
            users = User.objects.filter(nickname=nickname)
        elif email is not None:
            users = User.objects.filter(email=email)
        else:
            return None

        if len(users) == 0:
            return None

        user = users[0]
        if user.check_password(password):
            return user
        else:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None