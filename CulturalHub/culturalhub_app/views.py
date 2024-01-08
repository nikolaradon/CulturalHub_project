from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import CreateView, DeleteView
from django.urls import reverse_lazy
from culturalhub_app.models import UserProfile, Category, UserContent, Comment
from culturalhub_app.forms import RegistrationForm, UserProfileForm, ContentEditForm, CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout, login
from django.http import JsonResponse


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
            return redirect('main-page')
        return render(request, 'login.html', {'form': form})


class RegisterView(CreateView):
    """
    View uses Django's built-in CreateView to handle user registration.
    It renders a registration form using the RegistrationForm and creates a new UserProfile upon successful form submission.
    """
    model = UserProfile
    form_class = RegistrationForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        """
        Overrides the form_valid method to perform additional actions upon successful registration.
        In this case, it adds a success message to the request and calls the parent class's form_valid method.
        """
        response = super().form_valid(form)
        messages.success(self.request, "Profile has been successfully created. Please log in.")
        return response


def logout_view(request):
    """
    View for logging a user out.
    This view uses Django's `logout` function to log the user out and then redirects them to the login page.
    """
    logout(request)
    return redirect('login')


class MainPageView(View):
    """
    Class-based view for rendering the main page.
    """
    def get(self, request):
        """
        Handles GET requests for the main page.
        Retrieves all categories from the database.
        Fetches the current user from the request.
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
    """
    def get(self, request, user_id):
        """
        Handles GET requests for user profile details.

        :param user_id: ID of the user profile to display.
        """
        try:
            user_profile = UserProfile.objects.get(user=user_id)
            contents = UserContent.objects.filter(author=user_profile)

            grouped_contents = {}
            for content in contents:
                category = content.category
                if category not in grouped_contents:
                    grouped_contents[category] = []
                grouped_contents[category].append(content)

            ctx = {
                'user_profile': user_profile,
                'grouped_contents': grouped_contents
            }

            return render(request, 'user_profile.html', ctx)

        except UserProfile.DoesNotExist:
            messages.error(request, "User profile with this ID doesn't exist!")
            return redirect('main-page')


class UserProfileEditView(View, LoginRequiredMixin):
    """
    View responsible for editing a user profile.
    This view requires authentication, meaning that only logged-in users can edit their profiles.
    """
    def get(self, request, user_id):
        """
        Handles GET requests, checking if the user is logged in.
        If so, it retrieves the user profile and creates a UserProfileForm filled with profile data and user-related data (first name and last name).
        If the user is not logged in, it redirects them to the login page (login)
        If the logged-in user is not the owner of the profile, it returns a 403 Forbidden response.
        """
        if request.user.is_authenticated:
            user = get_object_or_404(User, id=user_id)

            if request.user == user:
                user_profile = user.userprofile
                form = UserProfileForm(instance=user_profile,
                                       initial={'first_name': user.first_name, 'last_name': user.last_name})

                return render(request, 'user_profile_edit.html', {'user_profile': user_profile, 'form': form})
            else:
                return HttpResponseForbidden("You do not have permission to edit this profile.")
        else:
            return redirect('login')

    def post(self, request, user_id):
        """
        Handles POST requests, which are used to save changes made in the profile editing form.
        If the form is valid, it saves the changes to the user profile and redirects them to their profile page.
        If the form is not valid, it re-renders the profile editing page with errors.
        """
        if request.user.is_authenticated:
            user = get_object_or_404(User, id=user_id)
            user_profile = user.userprofile
            form = UserProfileForm(request.POST, instance=user_profile)

            if form.is_valid():
                request.user.first_name = form.cleaned_data['first_name']
                request.user.last_name = form.cleaned_data['last_name']
                request.user.save()
                form.save()
                messages.success(request, "Profile has been updated successfully.")
                return redirect('user', user_id=user.id)
            else:
                return render(request, 'user_profile_edit.html', {'user_profile': user_profile, 'form': form})
        else:
            return redirect('login')


class CategoryContentView(View):
    """
    view responsible for handling GET requests to display contents belonging to a specific category.
    It retrieves the category object based on the provided category name and fetches all associated user contents.
    """
    def get(self, request, category):
        """
        Handles GET requests for displaying contents of a specific category.
        If the specified category does not exist, it adds an error message and redirects the user to the main page.

        :param category: The name of the category to retrieve and display contents.
        """
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
    """
    View is responsible for displaying detailed information about a specific content item.
    It retrieves the content with the given content_id from the database and renders the details along with its associated category.
    """
    def get(self, request, content_id):
        """
        Handles GET requests for displaying detailed information about a specific content item.
        If the content does not exist, it shows an error message and redirects the user to the main page.
        :param content_id: ID of the content to display.
        """
        try:
            content = UserContent.objects.get(id=content_id)
            category = content.category
            comments = Comment.objects.filter(commented_content=content)

            form = CommentForm()

            ctx = {
                'content': content,
                'category': category,
                'comments': comments,
                'form': form
            }
            return render(request, 'content.html', ctx)
        except UserContent.DoesNotExist:
            messages.error(request, 'Content does not exist!')
            return redirect('main-page')


class ContentCreateView(LoginRequiredMixin, CreateView):
    """
    View for creating new content.
    This view requires users to be logged in, as indicated by the LoginRequiredMixin.
    """
    model = UserContent
    fields = ['title', 'description', 'date', 'location', 'category', 'interests', 'culture', 'rating']
    template_name = 'create_content.html'
    login_url = 'login'

    def form_valid(self, form):
        """
        Handles a valid form submission.
        This method is called when the form is successfully validated. It saves the content object to the database
        and assigns the current user's UserProfile as the author. After saving, it redirects the user to the category
        page associated with the created content.
        """
        content = form.save(commit=False)
        content.author = self.request.user.userprofile
        content.save()
        category_name = content.category.name
        return redirect('category', category=category_name)


class EditContentView(LoginRequiredMixin, View):
    def get(self, request, content_id):
        try:
            content = UserContent.objects.get(id=content_id)
            form = ContentEditForm(instance=content)
        except UserContent.DoesNotExist:
            messages.error(request, "Content does not exist")
            return redirect('main-page')

        if request.user == content.author.user:
            return render(request, 'edit_content.html', {'content': content, 'form': form})
        else:
            return HttpResponseForbidden("You do not have permission to edit this content.")

    def post(self, request, content_id):
        content = UserContent.objects.get(id=content_id)

        if request.user == content.author.user:
            form = ContentEditForm(request.POST, instance=content)
            if form.is_valid():
                form.save()
                messages.success(request, "Content has been updated successfully.")
                return redirect('content-view', content_id)
            else:
                return render(request, 'edit_content.html', {'content': content, 'form': form})
        else:
            return HttpResponseForbidden("You do not have permission to edit this content.")


class DeleteContentView(LoginRequiredMixin, DeleteView):
    model = UserContent
    template_name = 'content_confirm_delete.html'
    success_url = reverse_lazy('main-page')

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj and obj.author == self.request.user.userprofile:
            return super().delete(request, *args, **kwargs)
        else:
            messages.error(request, "You do not have permission to delete this content.")
            return redirect('main-page')


class AddCommentView(View):
    def post(self, request, content_id):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user.userprofile
            comment.commented_content = UserContent.objects.get(id=content_id)
            comment.save()
        return redirect('content-view', content_id=content_id)




