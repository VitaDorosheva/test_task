from django.shortcuts import render, redirect
from .forms import RegistrationForm

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/confirm/')
        else:
            '''form is not valid'''
            form = RegistrationForm()

            args = {'form': form}
            return render(request, 'referral/register_form.html', args)
    else:
        form = RegistrationForm()

        args = {'form': form}
        return render(request, 'referral/register_form.html', args)
