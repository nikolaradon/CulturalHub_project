from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView
from django.urls import reverse_lazy
from culturalhub_app.models import UserProfile, Category, UserContent
from culturalhub_app.forms import RegistrationForm, UserProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout, login, authenticate


# Create your views here.


class LoginView(View):
    """
    Class-based view for user authentication and login.
    """
    def get(self, request):
        """
        Checks if the user is already authenticated.
        If authenticated, it redirects to the main page with an error message.
        If not authenticated, it renders the login page with an empty authentication form.
        """
        if request.user.is_authenticated:
            messages.error(request, "You are already logged in!")
            return redirect('main-page')

        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        """
        Validates the login form using the AuthenticationForm.
        If the form is valid, it retrieves the user, logs them in and redirects to the main page
        If the form is invalid does not proceed with login, renders the login page with the authentication form and error messages.
        """
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            print(f"User {user.username} logged in successfully.")
            return redirect('main-page')
        else:
            print("Invalid login attempt. Form errors:", form.errors)
            pass
        return render(request, 'login.html', {'form': form})



class RegisterView(CreateView):
    """
    View uses Django's built-in CreateView to handle user registration.
    It renders a registration form using the RegistrationForm and creates a new UserProfile upon successful form submission.

    Attributes:
        model (UserProfile): The model used for creating a new user profile.
        form_class (RegistrationForm): The form class responsible for handling user registration data.
        template_name (str): The name of the template used for rendering the registration page.
        success_url (str): The URL to redirect to upon successful user registration.

        Methods:
        form_valid(form): Overrides the form_valid method to add a success message upon successful registration.
    """
    model = UserProfile
    form_class = RegistrationForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        """
        Process a valid form submission.

        Overrides the form_valid method to perform additional actions upon successful registration.
        In this case, it adds a success message to the request and calls the parent class's form_valid method.

        :param form: RegistrationForm object.
        :return: HttpResponse object.
        """
        response = super().form_valid(form)
        messages.success(self.request, "Profile has been successfully created. Please log in.")
        return response


def logout_view(request):
    """
    View for logging a user out.
    This view uses Django's `logout` function to log the user out and then redirects them to the login page.

    :param request: HttpRequest object.
    :return: HttpResponse object.
    """
    logout(request)
    return redirect('login')


class MainPageView(View):
    """
    Class-based view for rendering the main page.

    Methods:
        get(request): Renders GET requests for the main page
    """
    def get(self, request):
        """
        Handles GET requests for the main page.
        Retrieves all categories from the database.
        Fetches the current user from the request.
        Renders the 'main.html' template with the categories and user information.

        :param request: HttpRequest object.
        :return: HttpResponse object.
        """
        categories = Category.objects.all()
        user = request.user
        ctx = {
            'categories': categories,
            'user': user
        }

        return render(request, 'main.html', ctx)


class UserProfileView(View):
    """
    View for displaying user profiles

    Methods:
        get(request, user_id): Handles GET requests for user profile details.
    """
    def get(self, request, user_id):
        """
        Handles GET requests for user profile details.

        :param request: HttpRequest object.
        :param user_id: ID of the user profile to display.
        :return: HttpResponse object.
        """
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
            form = UserProfileForm(instance=user_profile, initial = {'first_name':request.user.first_name, 'last_name': request.user.last_name})

            return render(request, 'user_profile_edit.html', {'user_profile': user_profile, 'form': form})
        else:
            return redirect('login')

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user_profile = request.user.userprofile
            form = UserProfileForm(request.POST, instance=user_profile)

            if form.is_valid():
                request.user.first_name = form.cleaned_data['first_name']
                request.user.last_name = form.cleaned_data['last_name']
                request.user.save()
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

