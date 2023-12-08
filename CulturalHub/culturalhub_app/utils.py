from django.contrib.auth.models import User
from faker import Faker
import random
from .models import UserProfile, Interest

fake = Faker()


def generate_sample_data():
    for _ in range(10):
        user = User.objects.create_user(
            username=fake.user_name(),
            password=fake.password(),
            email=fake.email(),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
        )

        UserProfile.objects.filter(
            user=user).update(
            birth_year=random.randint(1980, 2000),
            country=fake.country_code(),
            about=fake.paragraph(),
        )

        interests_count = random.randint(1, 13)
        user.userprofile.interests.set(random.choices(Interest.objects.all(), k=interests_count))

    print("Sample data for users has been created.")
