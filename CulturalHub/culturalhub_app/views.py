from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from culturalhub_app.models import UserProfile, Category, UserContent
from culturalhub_app.forms import RegistrationForm, UserProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout, login, authenticate


# Create your views here.


# class LoginView(View):
#     def get(self, request):
#         if request.user.is_authenticated:
#             messages.error(request, "You are already logged in!")
#             return redirect('main-page')
#
#         form = AuthenticationForm()
#         return render(request, 'login.html', {'form': form})
#
#     def post(self, request):
#         form = AuthenticationForm(request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             print(f"User {user.username} logged in successfully.")
#             return redirect('main-page')
#         else:
#             # print("Invalid login attempt. Form errors:", form.errors)
#             pass
#         return render(request, 'login.html', {'form': form})


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            messages.error(request, "You are already logged in!")
            return redirect('main-page')

        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"User {user.username} logged in successfully.")
            return redirect('main-page')
        else:
            messages.error(request, "Invalid login credentials. Please try again.")

        return render(request, 'login.html')


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
        categories = Category.objects.all()
        user = request.user
        ctx = {
            'categories': categories,
            'user': user
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


class UserProfileEditView(View, LoginRequiredMixin):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user_profile = request.user.userprofile
            form = UserProfileForm(instance=user_profile)
            return render(request, 'user_profile_edit.html', {'user_profile': user_profile, 'form': form})
        else:
            return redirect('login')

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user_profile = request.user.userprofile
            form = UserProfileForm(request.POST, instance=user_profile)

            if form.is_valid():
                form.save()
                messages.success(request, "Profile has been updated successfully.")
                return redirect('user', user_id=request.user.id)
            else:
                return render(request, 'user_profile_edit.html', {'user_profile': user_profile, 'form': form})
        else:
            return redirect('login')


class CategoryContentView(View):
    def get(self, request, category):
        try:
            category_obj = Category.objects.get(name=category)
            contents = UserContent.objects.filter(category__name=category)

            ctx = {
                'contents': contents,
                'category': category_obj
            }

            return render(request, 'category_content.html', ctx)

        except Category.DoesNotExist:
            messages.error(request, "Category does not exist!")
            return redirect('main-page')


class ContentView(View):
    def get(self, request, content_id):
        try:
            content = UserContent.objects.get(id=content_id)
            category = content.category

            ctx = {
                'content': content,
                'category': category
            }
            return render(request, 'content.html', ctx)
        except UserContent.DoesNotExist:
            messages.error(request, 'Content does not exist!')
            return redirect('main-page')


class ContentCreateView(LoginRequiredMixin, CreateView):
    model = UserContent
    fields = ['title', 'description', 'date', 'location', 'category', 'interests', 'culture', 'rating']
    template_name = 'create_content.html'
    login_url = 'login'

    def form_valid(self, form):
        content = form.save(commit=False)
        content.author = self.request.user.userprofile
        content.save()
        category_name = content.category.name
        return HttpResponseRedirect(reverse_lazy('category', kwargs={'category': category_name}))

