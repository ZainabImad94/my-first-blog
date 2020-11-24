from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistrationForm


def register(request):
    if request.method == 'POST':  # if the form has been submitted
        form = RegistrationForm(request.POST)  # form bound with post data
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created !')
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'accounts/registration.html', {'form': form})
