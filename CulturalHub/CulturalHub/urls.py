"""
URL configuration for CulturalHub project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from culturalhub_app.views import (LoginView, RegisterView, MainPageView,
                                   UserProfileView, CategoryContentView, UserProfileEditView,
                                   logout_view, ContentView)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('main/', MainPageView.as_view(), name='main-page'),
    path('user/<int:user_id>/', UserProfileView.as_view(), name='user'),
    path('category/<str:category>',CategoryContentView.as_view(), name='category'),
    path('edit/user/<int:user_id>', UserProfileEditView.as_view(), name='edit-user'),
    path('logout/', logout_view, name='logout'),
    path('content/<int:content_id>/', ContentView.as_view(), name='content-view')
]
