from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import RegistrationForm, PromoProfileForm
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
    if request.method == 'POST':

        form = PromoProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
        return redirect(reverse('view_profile'))
    else:

        try:
            user.profile
        except UserProfile.DoesNotExist:
            UserProfile.objects.create(user=user)
            return render(request, 'referral/confirm.html')
        if not user.profile.email_confirmed:
            return render(request, 'referral/confirm.html')
        promo_form = PromoProfileForm(instance=request.user.profile)
        args = {'user': user, 'promo_form': promo_form}
        return render(request, 'referral/profile.html', args)

def top10(request):
    tops = UserProfile.objects.order_by('points').reverse()[:10]
    top_list = []
    for top in tops:
        top_list.append({'user': top.user,
                         'points': top.points})
    return render(request, 'referral/top10.html', {'top_list': top_list})
