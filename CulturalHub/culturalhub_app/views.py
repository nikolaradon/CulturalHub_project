from django.contrib.auth.models import User
from django.http import request
from django.shortcuts import render
from django.views import View
from django.views.generic import FormView, CreateView, UpdateView
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from culturalhub_app.models import UserProfile, Category
from culturalhub_app.forms import RegistrationForm
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = 'login.html'
    success_url = reverse_lazy('main-page')


class RegisterView(CreateView):
    model = UserProfile
    form_class = RegistrationForm
    template_name = 'register.html'
    success_url = reverse_lazy('user-profile')


class MainPageView(View):
    def get(self, request):
        if request.method == 'GET':
            event = Category.objects.get(name='Event')
            tip = Category.objects.get(name='Tip')
            review = Category.objects.get(name='Place review')


            ctx = {
                'review': review,
                'tip': tip,
                'event': event,
                'user': request.user
            }

        return render(request, 'main.html', ctx)


class UserProfileView(View):
    def get(self, request, user_id):
        user_profile = UserProfile.objects.get(id=user_id)

        return render(request, 'user_profile.html', {'user_profile': user_profile})


class UserProfileEditView(UpdateView, LoginRequiredMixin):
    model = UserProfile
    fields = ['country', 'birth_year', 'about', 'interests']
    template_name = 'user_profile_edit.html'

    def get_success_url(self):
        user_id = self.request.user.id
        return reverse_lazy('user', kwargs={'user_id': user_id})

    def get_object(self, queryset=None):
        return UserProfile.objects.get(user=self.request.user)



class UserContentView(View):
    pass