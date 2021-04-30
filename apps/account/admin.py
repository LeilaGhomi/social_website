"""Integrate with admin module."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import User, Following, FriendRequest


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Define admin model for custom User model."""

    list_display = ('username', 'first_name', 'last_name', 'date_joined', 'is_active')
    search_fields = ('username', 'first_name', 'last_name')
    ordering = ('date_joined',)


@admin.register(FriendRequest)
class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ['from_user', 'to_user']


@admin.register(Following)
class FollowingAdmin(admin.ModelAdmin):
    list_display = ['user']