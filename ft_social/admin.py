from django.contrib import admin
from ft_social.models import Follow


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('left', 'right', 'created_at')
