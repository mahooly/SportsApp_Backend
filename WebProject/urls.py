"""WebProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import include
from django.urls import path
from rest_framework import routers
from SportsApp import views

router = routers.DefaultRouter()
router.register(r'news', views.NewsArticleListView, 'news')
router.register(r'teams', views.TeamListView, 'teams')
router.register(r'matches', views.MatchListView, 'matches')
router.register(r'players', views.PlayerListView, 'players')
router.register(r'leagues', views.NewsArticleListView, 'leagues')
router.register(r'register', views.UserCreate, 'register')
router.register(r'user_teams', views.UserTeamView, 'user_teams')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('rest-auth/', include('rest_auth.urls')),
]