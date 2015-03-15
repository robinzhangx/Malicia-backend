# coding=utf-8
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from ft_accounts.models import UserProfile


class ProfileInline(admin.StackedInline):
    model = UserProfile


class UserProfileAdmin(UserAdmin):
    inlines = [ProfileInline]
    list_display = ('id', 'nickname', 'email', 'is_active', 'date_joined', 'is_staff', 'fitting_count')
    list_display_links = ('id', 'nickname', 'email')
    list_filter = ('is_staff', 'is_superuser', 'groups')
    search_fields = ['email', 'username']

    def nickname(self, obj):
        return "%s" % obj.username
    nickname.short_description = u'昵称'

    def fitting_count(self, obj):
        return obj.fittings.count()
    fitting_count.short_description = u'Fitting数'


admin.site.unregister(User)
admin.site.register(User, UserProfileAdmin)