from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import OneTimeCode, UserProfile
from .settings import SITE_URL


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    users_count = User.objects.filter(is_staff=False).count()
    if users_count >= 5:
        promo_code_required = True
    else:
        promo_code_required = False
    promo_code = forms.CharField(required=promo_code_required)


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
            promo_code = self.cleaned_data['promo_code']
            user_profile = UserProfile.objects.get(user=user)
            if not user_profile:
                user_profile = UserProfile.objects.create(user=user)

            user_profile.promocode_used = promo_code
            user_profile.save()

            code_owner = UserProfile.objects.get(promocode_generated=promo_code)
            if code_owner:
                prize = code_owner.points + 1
            while code_owner and prize > 0:
                next_owner = UserProfile.objects.get(promocode_generated=code_owner.promocode_generated)
                if next_owner:
                    code_owner.points += 1
                    code_owner.save()
                    prize -= 1
                    code_owner = next_owner
                else:
                    code_owner.points += prize
                    code_owner.save()
                    prize = 0

            """creating one-time code for email confirmation"""

            otc = OneTimeCode.generate(user)

            text = f'''Please finish your resistration. Follow the link to confirm your email:
            {SITE_URL}/profile?otcode={otc.code}'''

            user.email_user('E-mail confirmation', text)

        return user


class PromoProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = (
            'promocode_generated',
        )

    def save(self, commit=True):

        profile = super(PromoProfileForm, self).save(commit=False)
        print(profile)
        profile.promocode_generated = profile.generate_promocode()

        if commit:
            profile.save()


        return profile.user
