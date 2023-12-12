from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from datetime import date
from .models import UserProfile


class RegistrationForm(UserCreationForm):
    birth_year = forms.IntegerField(label='Year of birth')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_birth_year(self):
        birth_year = self.cleaned_data.get('birth_year')
        today = date.today()
        age = today.year - birth_year
        if age < 18:
            raise forms.ValidationError("You must be at least 18 years old to register.")
        return birth_year

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already in use. Please use a different email address.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.full_clean()

        if commit:
            user.save()
            user_profile, created = UserProfile.objects.get_or_create(user=user)
            user_profile.birth_year = self.cleaned_data['birth_year']
            user_profile.save()

        return user


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['country', 'birth_year', 'about', 'interests']
