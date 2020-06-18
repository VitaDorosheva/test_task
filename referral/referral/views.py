from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.core.exceptions import ValidationError


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
