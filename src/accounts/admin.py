from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from accounts.models import (
    UserProfile,
    Skill,
    UserSkill,
    Entity,
)


class ProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'profile'


class UserAdmin(UserAdmin):
    inline = (ProfileInline, )


@admin.register(UserSkill)
class UserSkillAdmin(admin.ModelAdmin):
    fields = ('profile', 'skill', 'level')

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Entity)
admin.site.register(Skill)
admin.site.register(UserProfile)
