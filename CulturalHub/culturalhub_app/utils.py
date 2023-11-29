from django.contrib.auth.models import User
from faker import Faker
import random
from .models import UserProfile, Interest

fake = Faker()


def generate_sample_data():
    for _ in range(10):
        try:
            user = User.objects.create_user(
                username=fake.user_name(),
                password=fake.password(),
                email=fake.email(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
            )

            profile = UserProfile(
                user=user,
                age=random.randint(18, 60),
                country=fake.country_code(),
                about=fake.paragraph(),
            )
            profile.save()

            # Dodawanie zainteresowań
            interests_count = random.randint(1, 13)
            profile.interests.set(random.sample(Interest.objects.all(), interests_count))

        except Exception as e:
            print(f"Error creating user: {e}")

    print("Sample data for users has been created.")