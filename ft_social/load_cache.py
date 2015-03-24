from ft_social.models import Follow


def load_relations():
    for f in Follow.objects.all():
        f.populate_cache()
