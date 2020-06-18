import random
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class OneTimeCode(models.Model):
    code = models.CharField(max_length=64,
                            primary_key=True)
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)

    @classmethod
    def generate(cls, user):
        chars = 'abcdefghijklnopqrstuvwxyz1234567890'
        length = 64
        code = ''
        for n in range(length):
            code += random.choice(chars)

        return cls.objects.create(code=code, user=user)


class UserProfile(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='profile')
    email_confirmed = models.BooleanField(default=False)
    promocode_generated = models.CharField(max_length=255,
                                           null=True,
                                           blank=True)
    promocode_used = models.CharField(max_length=255,
                                      null=True,
                                      blank=True)

    class Meta:
        verbose_name = 'User profile'
        verbose_name_plural = 'User profiles'

    def __str__(self):
        return self.user.username

    def generate_promocode(self):
        """generetes random codes like 'aaa-BBB-999'
           with pairs, delimited by delimiter """
        if self.promocode_generated:
            return
        pairs = 4
        digits = 6
        delimiter = '-'
        chars = 'abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'

        codes = []
        for n in range(pairs):
            pair = ''
            for d in range(digits):
                pair += random.choice(chars)
            codes.append(pair)
        code = delimiter.join(codes)
        self.promocode_generated = code

def create_profile(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        user_profile = UserProfile(user=user)
        user_profile.save()

post_save.connect(create_profile, sender=User)
