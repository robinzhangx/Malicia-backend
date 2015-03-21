from django.utils.datetime_safe import datetime
from django.db import models
from fitting.redis_store import redis_store
from ft_accounts.models import User
from ft_accounts.serializers import UserSerializer


class Follow(models.Model):
    left = models.ForeignKey(User, related_name='following_relations')
    right = models.ForeignKey(User, related_name='followed_by_relations')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            ('left', 'right')
        )

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(Follow, self).save(force_insert=force_insert, force_update=force_update, using=using,
             update_fields=update_fields)

        timestamp = (datetime.utcnow() - datetime(1970, 1, 1)).total_seconds()

        redis_store.zadd('following_%s' % str(self.left.id), timestamp, UserSerializer(self.right).data)
        redis_store.zadd('followed_by_%s' % str(self.right.id), timestamp, UserSerializer(self.left).data)

    def __unicode__(self):
        return "{0} -> {1}".format(self.left, self.right)
