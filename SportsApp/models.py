from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class NewsArticle(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    text = models.TextField()
    image = models.ImageField(upload_to='../media/news', null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=10)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date']


class Comment(models.Model):
    article = models.ForeignKey(NewsArticle, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name + ': ' + self.user.username


class League(models.Model):
    name = models.CharField(max_length=30)
    type = models.CharField(max_length=10)
    is_ongoing = models.BooleanField(default=True)
    start_date = models.DateField()
    logo = models.ImageField(upload_to='../media/leagues')

    def __str__(self):
        return self.name + str(self.start_date.year)


class Team(models.Model):
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=10)
    logo = models.ImageField(upload_to='../media/teams')
    leagues = models.ManyToManyField(League)

    def __str__(self):
        return self.name


class CoachingStaff(models.Model):
    team = models.OneToOneField(Team, on_delete=models.CASCADE, related_name='coaching_staff')
    caretaker_manager = models.CharField(max_length=30)
    first_team_coach = models.CharField(max_length=30)
    assistant_coaches = models.CharField(max_length=200)
    goalkeeping_coach = models.CharField(max_length=30)
    fitness_coach = models.CharField(max_length=30)
    head_analysis = models.CharField(max_length=30)
    head_development = models.CharField(max_length=30)

    def __str__(self):
        return self.team.name + ' Coaching Staff'

    class Meta:
        verbose_name_plural = 'Coaching Staff'


class Player(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    height = models.IntegerField()
    weight = models.FloatField()
    nationality = models.CharField(max_length=50)
    image = models.ImageField(upload_to='../media/players')

    def __str__(self):
        return self.name


class PlayerSeason(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='stats')
    season = models.CharField(max_length=50)


class PlayerStat(models.Model):
    player_season = models.ForeignKey(PlayerSeason, on_delete=models.CASCADE, related_name='stats')
    name = models.CharField(max_length=100)
    value = models.IntegerField()


class TeamPosition(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='players')
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='teams')
    position = models.CharField(max_length=20)

    def __str__(self):
        return self.player.name + ' - ' + self.team.name


class Match(models.Model):
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team1')
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team2')
    type = models.CharField(max_length=10)
    score1 = models.IntegerField()
    score2 = models.IntegerField()
    has_commentary = models.BooleanField(default=False)
    date = models.DateTimeField()
    player1 = models.ManyToManyField(TeamPosition, related_name='player1')
    player2 = models.ManyToManyField(TeamPosition, related_name='player2')
    sub1 = models.ManyToManyField(TeamPosition, related_name='sub1')
    sub2 = models.ManyToManyField(TeamPosition, related_name='sub2')
    league = models.ForeignKey(League, on_delete=models.CASCADE)

    def __str__(self):
        return self.team1.name + ' - ' + self.team2.name

    class Meta:
        verbose_name_plural = 'Matches'


class MatchEvent(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='events')
    title = models.CharField(max_length=30)
    time = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.match) + ': ' + self.title + ' ' + str(((self.time - self.match.date).total_seconds() % 3600) // 60)

    class Meta:
        verbose_name_plural = 'Match Events'


class MatchStats(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='stats')
    name = models.CharField(max_length=40)
    first = models.IntegerField()
    second = models.IntegerField()

    def __str__(self):
        return str(self.match) + ' - ' + self.name

    class Meta:
        verbose_name_plural = 'Match Stats'


class UserFollowTeam(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'team')


class UserFollowPlayer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'player')