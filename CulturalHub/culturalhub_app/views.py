from django.shortcuts import render
from django.views import View
from django.views.generic import FormView, CreateView
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from culturalhub_app.models import UserProfile

# Create your views here.


class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = 'login.html'
    success_url = reverse_lazy('main-page')


class RegisterView(CreateView):
    model = UserProfile
    fields = '__all__'
    template_name = 'register.html'
    success_url = reverse_lazy('user-profile')


class MainPageView(View):
    pass