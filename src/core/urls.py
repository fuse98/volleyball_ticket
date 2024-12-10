"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

from users.views import UserRegistrationView, AuthTokenView
from matches.views import StadiumCreateView, SeatingArrangementCreateView, MatchCreateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/register/', UserRegistrationView.as_view(), name='users_registration'),
    path('users/auth-token/', AuthTokenView.as_view(), name='users_auth_token'),
    path('matches/stadium/create/', StadiumCreateView.as_view(), name='matches_stadium_create'),
    path(
        'matches/seating-arrangement/create/',
        SeatingArrangementCreateView.as_view(),
        name='matches_seating_arrangement_create'
    ),
    path('matches/match/create/', MatchCreateView.as_view(), name='matches_match_create'),
]
