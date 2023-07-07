"""
URL configuration for NewsPaper project.

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
from django.urls import path, include
from news.views import ForUsersView, upgrade_me, CategoryView, subscribe, unsubscribe, UserDataChanger
from accounts.views import ProfileView
from django.contrib.auth.views import PasswordChangeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('news/', include('news.urls')),
    path('articles/', include('news.urls')),
    path('accounts/', include('allauth.urls')),
    path('for-users/', ForUsersView.as_view()),
    path('for-users/upgrade/', upgrade_me, name='update'),
    path('accounts/profile/', ProfileView.as_view()),
    path('accounts/profile/password_change/', PasswordChangeView.as_view(
        template_name='change-password.html',
        success_url='/accounts/profile/'
    ), name='password_change'),
    # path('accounts/profile/password-change/done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    # path('accounts/profile/<int:pk>/', UserDataChanger.as_view()),
    path('categories/', CategoryView.as_view()),
    path('categories/subscribe/', subscribe, name='subscribe'),
    path('categories/unsubscribe/', unsubscribe, name='unsubscribe'),
]
