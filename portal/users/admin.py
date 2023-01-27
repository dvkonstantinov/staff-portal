from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group as DefaultGroup
from django.contrib.sites.models import Site

from users.models import Group, Profile

admin.site.unregister(DefaultGroup)
admin.site.unregister(Site)

User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = ('username', 'email', 'first_name', 'last_name',
                    'patronymic', 'is_staff', 'is_admin', 'is_active',
                    'verified', )
    search_fields = ('first_name', 'last_name', 'email',)


class ProfileInline(admin.StackedInline):
    model = Profile


class ExtendedUserAdmin(UserAdmin):
    inlines = UserAdmin.inlines + (ProfileInline,)


class GroupAdmin(admin.ModelAdmin):
    model = Group
    list_display = ('id', 'title', 'slug')


admin.site.register(User, ExtendedUserAdmin)
admin.site.register(Group, GroupAdmin)
