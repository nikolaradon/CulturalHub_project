from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import FormView, CreateView, UpdateView
from django.urls import reverse_lazy
from culturalhub_app.models import UserProfile, Category
from culturalhub_app.forms import RegistrationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout, authenticate, login


# Create your views here.


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            messages.error(request, "You are already logged in!")
            return redirect('main-page')

        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            print(f"User {user.username} logged in successfully.")
            return redirect('main-page')
        else:
            print("Invalid login attempt. Form errors:", form.errors)
        return render(request, 'login.html', {'form': form})


class RegisterView(CreateView):
    model = UserProfile
    form_class = RegistrationForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Profile has been successfully created. Please log in.")
        return response


def logout_view(request):
    logout(request)
    return redirect('login')


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
        try:
            user_profile = UserProfile.objects.get(user=user_id)
            return render(request, 'user_profile.html', {'user_profile': user_profile})
        except UserProfile.DoesNotExist:
            messages.error(request, "User profile with this ID doesn't exist!")
            return redirect('main-page')



class UserProfileEditView(UpdateView, LoginRequiredMixin):
    model = UserProfile
    fields = ['country', 'birth_year', 'about', 'interests']
    template_name = 'user_profile_edit.html'

    def get_success_url(self):
        return reverse_lazy('user', kwargs={'user_id': self.object.user.id})

    def get_object(self):
        return self.request.user.userprofile



class UserContentView(View):
    def get(self, request):
        pass
