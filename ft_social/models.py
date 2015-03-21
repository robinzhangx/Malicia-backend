from django.utils.datetime_safe import datetime
from django.db import models
from fitting.redis_store import redis_store
from ft_accounts.models import User
from ft_accounts.serializers import UserSerializer
from ft_notification.utils import create_notification


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

        redis_store.zadd('following_%s' % str(self.left.id), self.right.id, UserSerializer(self.right).data)
        redis_store.zadd('followed_by_%s' % str(self.right.id), self.left.id, UserSerializer(self.left).data)

        create_notification(self.right.id, {
            "type": "new_follower",
            "follower": self.left.id,  # TODO Check whether we need to add some user info here
        })

    def delete(self, using=None):
        super(Follow, self).delete(using=using)
        redis_store.zremrangebyscore('following_%s' % str(self.left.id), self.right.id, self.right.id)
        redis_store.zremrangebyscore('followed_by_%s' % str(self.right.id), self.left.id, self.left.id)

    def __unicode__(self):
        return "{0} -> {1}".format(self.left, self.right)
