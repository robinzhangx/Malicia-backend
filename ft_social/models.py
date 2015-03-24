from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils.datetime_safe import datetime
from django.db import models
import pytz
from fitting.redis_store import redis_store
from ft_accounts.models import User
from ft_notification.utils import create_notification


class Follow(models.Model):
    left = models.ForeignKey(User, related_name='following_relations')
    right = models.ForeignKey(User, related_name='followed_by_relations')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            ('left', 'right')
        )

    def populate_cache(self):
        timestamp = (self.created_at - datetime(1970, 1, 1, tzinfo=pytz.utc)).total_seconds()
        redis_store.zadd('following_{0}'.format(self.left_id), timestamp, self.right_id)
        redis_store.zadd('followers_{0}'.format(self.right_id), timestamp, self.left_id)

        create_notification(self.right.id, {
            "type": "new_follower",
            "follower": self.left.id,  # TODO Check whether we need to add some user info here
        })

    def remove_cache(self):
        redis_store.zrem('following_{0}'.format(self.left_id), self.right_id)
        redis_store.zrem('followers_{0}'.format(self.right_id), self.left_id)

    def __unicode__(self):
        return "{0} -> {1}".format(self.left, self.right)


@receiver(models.signals.post_save, sender=Follow)
def populate_cache(sender, instance, **kwargs):
    instance.populate_cache()


@receiver(models.signals.post_delete, sender=Follow)
def remove_cache(sender, instance, **kwargs):
    instance.remove_cache()
