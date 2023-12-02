from datetime import date
from django.db import models
from django_countries.fields import CountryField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Login', unique=True)
    country = CountryField(verbose_name='Country', null=True)
    birth_year = models.IntegerField(verbose_name='Birth Year', default=2000)
    about = models.TextField(verbose_name='About', null=True, blank=True)
    interests = models.ManyToManyField('Interest', verbose_name='Interests', blank=True, null=True)
    # avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Avatar')

    @property
    def age(self):
        today = date.today()
        return today.year - self.birth_year

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.userprofile.save()

    def __str__(self):
        return self.user.username


class Interest(models.Model):
    name = models.CharField(max_length=64, verbose_name='Interest')

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=64, verbose_name='Category name')
    description = models.TextField(verbose_name='Category description')

    def __str__(self):
        return self.name


class UserContent(models.Model):
    title = models.CharField(max_length=255, verbose_name='Title')
    description = models.TextField(verbose_name='Description')
    date = models.DateField(verbose_name='Date', blank=True, null=True)
    location = models.CharField(max_length=255, verbose_name='Location', blank=True)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='Organizer')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Category')
    interests = models.ManyToManyField('Interest', verbose_name='Interests')
    culture = models.CharField(max_length=255, verbose_name='Culture')
    rating = models.DecimalField(
        max_digits=3, decimal_places=2,
        verbose_name='Rating', null=True, blank=True
    )

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='User')
    commented_content = models.ForeignKey(UserContent, on_delete=models.CASCADE, verbose_name='commented_content')
    text = models.TextField(verbose_name='Comment')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')

    def __str__(self):
        return f'{self.user.user.username} - {self.created_at}'
