from django.contrib import admin
from .models import UserProfile, Interest, Category, UserContent, Comment
# Register your models here.

admin.site.register(Interest)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


@admin.register(UserProfile)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'country', 'age', 'about', 'display_interests')

    def display_interests(self, obj):
        return ", ".join([interest.name for interest in obj.interests.all()])

    display_interests.short_description = 'Interests'


@admin.register(UserContent)
class UserContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'date', 'location', 'author', 'category', 'display_interests', 'culture', 'rating')

    def display_interests(self, obj):
        return ", ".join([interest.name for interest in obj.interests.all()])

    display_interests.short_description = 'Interests'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'commented_content', 'text', 'created_at')
