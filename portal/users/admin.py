from django.contrib import admin
from django.contrib.auth import get_user_model

from users.models import Profile
User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = ('username', 'email', 'first_name', 'last_name',
                    'patronymic', 'is_staff',  'is_admin', 'is_active',
                    'verified', )
    search_fields = ('first_name', 'last_name', 'email',)


class ProfileInline(admin.StackedInline):
    model = Profile


class ExtendedUserAdmin(UserAdmin):
    inlines = UserAdmin.inlines + (ProfileInline,)


admin.site.register(User, ExtendedUserAdmin)
