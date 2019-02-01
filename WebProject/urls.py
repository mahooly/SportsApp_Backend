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
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, re_path
from django.urls import path
from rest_framework import routers
from SportsApp import views
from WebProject import settings
from rest_framework_jwt.views import obtain_jwt_token
from rest_auth.registration.views import VerifyEmailView, RegisterView, LoginView
from rest_auth.views import PasswordResetView, PasswordResetConfirmView


router = routers.DefaultRouter()
router.register(r'news', views.NewsArticleListView, 'news')
router.register(r'teams', views.TeamListView, 'teams')
router.register(r'matches', views.MatchListView, 'matches')
router.register(r'players', views.PlayerListView, 'players')
router.register(r'leagues', views.NewsArticleListView, 'leagues')
router.register(r'register', views.UserCreate, 'register')
router.register(r'user_teams', views.UserTeamView, 'user_teams')
router.register(r'user_players', views.UserPlayerView, 'user_players')
router.register(r'comments', views.CommentView, 'comments')

urlpatterns = [
    path('admin/', admin.site.urls),
    url('^api/matches/(?P<name>.+)/$', views.TeamMatchList.as_view()),
    path('api/', include(router.urls)),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/login/', LoginView.as_view(), name='account_login'),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('registration/', RegisterView.as_view(), name='account_signup'),
    path('rest-auth/password/reset/', PasswordResetView.as_view(), name='password_reset'),
    re_path(
        r'^rest-auth/password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    re_path(r'^rest-auth/registration/account-confirm-email/', VerifyEmailView.as_view(),
            name='account_email_verification_sent'),
    re_path(r'^rest-auth/registration/account-confirm-email/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', VerifyEmailView.as_view(),
            name='account_confirm_email'),
    path('token-auth/', obtain_jwt_token)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
