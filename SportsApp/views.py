from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *
from rest_framework import filters
from rest_framework import viewsets
from .serializers import *
from .filters import NewsFilterBackend


class NewsArticleListView(viewsets.ModelViewSet):
    serializer_class = NewsArticleSerializer
    queryset = NewsArticle.objects.all()
    filter_backends = (NewsFilterBackend, filters.SearchFilter,)
    search_fields = ('title', 'text', 'tags__name', 'type')


class PlayerListView(viewsets.ModelViewSet):
    serializer_class = PlayerSerializer
    queryset = Player.objects.all()


class TeamListView(viewsets.ModelViewSet):
    serializer_class = TeamSerializer
    queryset = Team.objects.all()


class MatchListView(viewsets.ModelViewSet):
    serializer_class = MatchSerializer
    queryset = Match.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('team1__name', 'team2__name')


class LeagueListView(viewsets.ModelViewSet):
    serializer_class = LeagueSerializer
    queryset = League.objects.all()


class UserCreate(viewsets.ViewSet):
    def create(self, request, format='json'):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserTeamView(viewsets.ModelViewSet):
    serializer_class = UserTeamSerializer

    def get_queryset(self):
        user = self.request.user
        return UserFollowTeam.objects.filter(user=user)


class UserPlayerView(viewsets.ModelViewSet):
    serializer_class = UserPlayerSerializer

    def get_queryset(self):
        user = self.request.user
        return UserFollowPlayer.objects.filter(user=user)