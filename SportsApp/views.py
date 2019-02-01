from django.db.models import Q
from django.shortcuts import render
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *
from rest_framework import filters
from rest_framework import viewsets
from .serializers import *
from .filters import NewsFilterBackend, MatchOrderingFilterBackend


class NewsArticleListView(viewsets.ModelViewSet):
    serializer_class = NewsArticleSerializer
    queryset = NewsArticle.objects.all()
    filter_backends = (NewsFilterBackend, filters.SearchFilter,)
    search_fields = ('title', 'text', 'tags__name', 'type')


class CommentView(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def create(self, request, *args, **kwargs):
        user = request.user
        article = NewsArticle.objects.get(id=request.data['id'])
        Comment.objects.create(user=user, article=article, name=request.data['name'], text=request.data['text'])
        return Response(status=status.HTTP_201_CREATED)


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
    search_fields = ('team1__name', 'team2__name', 'league__name')


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

    def create(self, request, *args, **kwargs):
        user = request.user
        team_id = request.data['team']
        team = Team.objects.get(id=team_id)
        UserFollowTeam.objects.create(user=user, team=team)
        return Response(status=status.HTTP_201_CREATED)


class UserPlayerView(viewsets.ModelViewSet):
    serializer_class = UserPlayerSerializer

    def get_queryset(self):
        user = self.request.user
        return UserFollowPlayer.objects.filter(user=user)

    def create(self, request, *args, **kwargs):
        user = request.user
        player_id = request.data['player']
        player = Player.objects.get(id=player_id)
        UserFollowPlayer.objects.create(user=user, player=player)
        return Response(status=status.HTTP_201_CREATED)


class TeamMatchList(generics.ListAPIView):
    serializer_class = MatchSerializer
    filter_backends = (MatchOrderingFilterBackend,)

    def get_queryset(self):
        name = self.kwargs['name']
        return Match.objects.filter(Q(team1__name=name) | Q(team2__name=name))
