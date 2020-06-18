from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm
from .models import UserProfile


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/confirm/')
        else:
            '''form is not valid'''
            print('form is not valid')
            raise ValidationError(form.errors)
            # form = RegistrationForm()
            #
            # args = {'form': form}
            # return render(request, 'referral/register_form.html', args)
    else:
        form = RegistrationForm()

        args = {'form': form}
        return render(request, 'referral/register_form.html', args)

@login_required
def user_profile(request, pk=None):
    if pk:
        user = User.objects.get(pk=pk)
    else:
        user = request.user
    try:
        user.profile
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=user)
        return render(request, 'referral/confirm.html')
    if not user.profile.email_confirmed:
        return render(request, 'referral/confirm.html')
    args = {'user': user}
    return render(request, 'referral/profile.html', args)
