from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .forms import RegisterForm
# Create your views here.

def register_view(request):
    if request.method =='POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password1 = form.cleaned_data['password1']

            User.objects.create_user(
                username=username,
                first_name = first_name,
                last_name = last_name,
                password = password1,
                email= email,
            )
            return redirect('login')
    else:
        form = RegisterForm()

    context = {'form':form}
    return render(request , 'accounts/register.html', context)