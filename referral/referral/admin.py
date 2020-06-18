from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile


class UserInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Additional info'


class UserAdmin(UserAdmin):
    inlines = (UserInline, )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_email_confirmed')

    def get_email_confirmed(self, instance):
        return instance.profile.email_confirmed

    get_email_confirmed.short_description = 'E-mail confirmed'


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
