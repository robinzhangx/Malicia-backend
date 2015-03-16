# coding=utf-8
from django.contrib import admin
from django.contrib.admin import ModelAdmin
from ft_accounts.models import User, WeixinAccount


class WeixinInline(admin.StackedInline):
    model = WeixinAccount


@admin.register(User)
class FTUserAdmin(ModelAdmin):
    inlines = [WeixinInline]
    list_display = ('id', 'nickname', 'email', 'is_active', 'date_joined', 'is_staff', 'fitting_count')
    list_display_links = ('id', 'nickname', 'email')
    list_filter = ('is_staff', 'is_superuser', 'groups')
    search_fields = ['email', 'nickname']

    def fitting_count(self, obj):
        return obj.fittings.count()
    fitting_count.short_description = u'Fitting数'
