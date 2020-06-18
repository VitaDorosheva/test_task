import random
from django.db import models
from django.contrib.auth.models import User


class OneTimeCode(models.Model):
    code = models.CharField(max_length=64,
                            primary_key=True)
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)

    @classmethod
    def generate(cls, user):
        chars = 'abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
        length = 64
        code = ''
        for n in range(length):
            code += random.choice(chars)

        return cls.objects.create(code=code, user=user)