from django.contrib.auth.models import User
from faker import Faker
import random
from .models import UserProfile, Interest

fake = Faker()


def generate_sample_data():
    """
    The sample data generation script creates fictional user data for testing and development purposes.
    It utilizes the Faker library to generate random and realistic-looking data, and it populates the User and UserProfile models in the Django application.
    """
    for _ in range(10):
        # Create a new user with random data
        user = User.objects.create_user(
            username=fake.user_name(),
            password=fake.password(),
            email=fake.email(),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
        )

        # Update the user's profile with additional random data
        UserProfile.objects.filter(
            user=user).update(
            birth_year=random.randint(1980, 2000),
            country=fake.country_code(),
            about=fake.paragraph(),
        )

        # Set a random number of interests for the user
        interests_count = random.randint(1, 13)
        user.userprofile.interests.set(random.choices(Interest.objects.all(), k=interests_count))

    print("Sample data for users has been created.")
