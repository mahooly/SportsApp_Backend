from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import *
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')


class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(min_length=8)

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'],
                                        validated_data['password'])
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name',)


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('user', 'name', 'text', 'date')


class NewsArticleSerializer(serializers.ModelSerializer):
    tags = TagSerializer(read_only=True, many=True)
    comments = CommentSerializer(many=True)

    class Meta:
        model = NewsArticle
        fields = ('id', 'title', 'description', 'text', 'date', 'tags', 'comments', 'image')


class TeamPositionSerializer(serializers.ModelSerializer):
    team = serializers.SlugRelatedField(read_only=True, slug_field='name')

    class Meta:
        model = TeamPosition
        fields = ('team', 'position')


class PlayerIDSerializer(serializers.ModelSerializer):

    class Meta:
        model = Player
        fields = ('id', 'name')


class PlayerPositionSerializer(serializers.ModelSerializer):
    player = PlayerIDSerializer(read_only=True)

    class Meta:
        model = TeamPosition
        fields = ('player', 'position')


class PlayerStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerStat
        exclude = ('id', 'player_season')


class PlayerSeasonSerializer(serializers.ModelSerializer):
    stats = PlayerStatSerializer(many=True)

    class Meta:
        model = PlayerSeason
        exclude = ('id', 'player')


class PlayerSerializer(serializers.ModelSerializer):
    teams = TeamPositionSerializer(many=True)
    stats = PlayerSeasonSerializer(many=True)

    class Meta:
        model = Player
        fields = '__all__'


class CoachingStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoachingStaff
        exclude = ('id', 'team')


class TeamSerializer(serializers.ModelSerializer):
    players = PlayerPositionSerializer(many=True)
    leagues = serializers.SlugRelatedField(read_only=True, slug_field='name', many=True)
    coaching_staff = CoachingStaffSerializer(required=True)

    class Meta:
        model = Team
        fields = '__all__'


class MatchStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchStats
        exclude = ('id', 'match')


class MatchEventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchEvent
        exclude = ('match', 'id')


class MatchTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('id', 'name', 'logo')


class MatchSerializer(serializers.ModelSerializer):
    team1 = MatchTeamSerializer(read_only=True)
    team2 = MatchTeamSerializer(read_only=True)
    player1 = PlayerPositionSerializer(many=True)
    player2 = PlayerPositionSerializer(many=True)
    sub1 = PlayerPositionSerializer(many=True)
    sub2 = PlayerPositionSerializer(many=True)
    league = serializers.SlugRelatedField(read_only=True, slug_field='name')
    events = MatchEventsSerializer(many=True)
    stats = MatchStatsSerializer(many=True)

    class Meta:
        model = Match
        fields = '__all__'


class LeagueSerializer(serializers.ModelSerializer):
    class Meta:
        model = League
        fields = '__all__'


class UserTeamSerializer(serializers.ModelSerializer):
    team = serializers.SlugRelatedField(read_only=True, slug_field='name')

    class Meta:
        model = UserFollowTeam
        fields = ('team',)


class UserPlayerSerializer(serializers.ModelSerializer):
    player = serializers.SlugRelatedField(read_only=True, slug_field='name')

    class Meta:
        model = UserFollowTeam
        fields = ('player',)
