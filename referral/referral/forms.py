from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import OneTimeCode, UserProfile
from .settings import SITE_URL


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)


    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        )

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
            #UserProfile.objects.get_or_create(user=user)
        """creating one-time code for email confirmation"""

        otc = OneTimeCode.generate(user)

        text = f'''Please finish your resistration. Follow the link to confirm your email:
        {SITE_URL}/profile?otcode={otc.code}'''

        user.email_user('E-mail confirmation', text)

        return user
