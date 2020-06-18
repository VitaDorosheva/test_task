from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
from .models import OneTimeCode


class OneTimeCodeBackend(ModelBackend):

    def authenticate(self, request, token):
        if not token:
            return None
        try:
            otcode = OneTimeCode.objects.get(pk=token)
        except OneTimeCode.DoesNotExist:
            return None

        user = otcode.user
        user.profile.email_confirmed = True
        user.profile.save(update_fields=['email_confirmed'])

        otcode.delete()
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None