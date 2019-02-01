from django.conf.urls import url
from django.contrib import admin
from django.db.models import Sum, Count
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.html import format_html
from .forms import AddEventForm
from .models import *
from datetime import datetime, timedelta


class MatchEventInline(admin.TabularInline):
    model = MatchEvent
    readonly_fields = ('time',)
    fields = ('title', 'comment')


class MatchStatsInline(admin.StackedInline):
    model = MatchStats


class TypeFilter(admin.SimpleListFilter):
    title = 'type'
    parameter_name = 'type'

    def lookups(self, request, model_admin):
        return (
            ('Football', 'Football'),
            ('Basketball', 'Basketball'),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'Football':
            return queryset.filter(type='فوتبال')
        elif value == 'Basketball':
            return queryset.exclude(type='فوتبال')
        return queryset


class MatchOngoingFilter(admin.SimpleListFilter):
    title = 'is Ongoing'
    parameter_name = 'is Ongoing'

    def lookups(self, request, model_admin):
        return (
            ('Live', 'Live'),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'Live':
            time_threshold = datetime.now() - timedelta(minutes=120)
            return queryset.filter(date__gt=time_threshold)


class MatchAdmin(admin.ModelAdmin):
    list_display = ['name', 'increase_score_one', 'team1_name', 'score1', 'score2', 'team2_name', 'increase_score_two',
                    'event_actions']
    inlines = [MatchEventInline, MatchStatsInline]
    list_filter = [TypeFilter, MatchOngoingFilter, 'date']
    search_fields = ['team1_name', 'team2_name']

    def name(self, obj):
        return str(obj)

    def team1_name(self, obj):
        return obj.team1.name

    def team2_name(self, obj):
        return obj.team2.name

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            url(
                r'^(?P<match_id>.+)/add_event/$',
                self.admin_site.admin_view(self.process_event),
                name='add_event',
            ),
            url(
                r'^(?P<match_id>.+)/increase_scoreOne_1/$',
                self.admin_site.admin_view(self.process_addOne_one),
                name='add_scoreOne_one',
            ),
            url(
                r'^(?P<match_id>.+)/increase_scoreOne_2/$',
                self.admin_site.admin_view(self.process_addOne_two),
                name='add_scoreOne_two',
            ),
            url(
                r'^(?P<match_id>.+)/increase_scoreOne_3/$',
                self.admin_site.admin_view(self.process_addOne_three),
                name='add_scoreOne_three',
            ),
            url(
                r'^(?P<match_id>.+)/increase_scoreTwo_1/$',
                self.admin_site.admin_view(self.process_addTwo_one),
                name='add_scoreTwo_one',
            ),
            url(
                r'^(?P<match_id>.+)/increase_scoreTwo_2/$',
                self.admin_site.admin_view(self.process_addTwo_two),
                name='add_scoreTwo_two',
            ),
            url(
                r'^(?P<match_id>.+)/increase_scoreTwo_3/$',
                self.admin_site.admin_view(self.process_addTwo_three),
                name='add_scoreTwo_three',
            ),
        ]
        return custom_urls + urls

    def event_actions(self, obj):
        return format_html(
            '<a class="button" href="{}">Add Event</a>&nbsp;',
            reverse('admin:add_event', args=[obj.pk]),
        )

    event_actions.short_description = 'Event Actions'
    event_actions.allow_tags = True

    def process_event(self, request, match_id, *args, **kwargs):
        return self.process_action(
            request=request,
            match_id=match_id,
            action_form=AddEventForm,
            action_title='Add Event',
        )

    def process_action(self, request, match_id, action_form, action_title):
        match = self.get_object(request, match_id)
        if request.method != 'POST':
            form = action_form()
        else:
            form = action_form(request.POST)
            if form.is_valid():
                event = form.save(commit=False)
                event.match = match
                event.save()
                self.message_user(request, 'Event Added Successfuly')
                return HttpResponseRedirect('/admin/SportsApp/match')

        context = self.admin_site.each_context(request)
        context['opts'] = self.model._meta
        context['form'] = form
        context['match'] = match
        context['title'] = action_title
        return TemplateResponse(
            request,
            'admin/match/event_action.html',
            context,
        )

    def increase_score_one(self, obj):
        if obj.type == 'بسکتبال':
            return format_html(
                '<a class="button" href="{}">Add 1</a>&nbsp;'
                '<a class="button" href="{}">Add 2</a>&nbsp;'
                '<a class="button" href="{}">Add 3</a>',
                reverse('admin:add_scoreOne_one', args=[obj.pk]),
                reverse('admin:add_scoreOne_two', args=[obj.pk]),
                reverse('admin:add_scoreOne_three', args=[obj.pk])
            )
        elif obj.type == 'فوتبال':
            return format_html(
                '<a class="button" href="{}">Add 1</a>&nbsp;',
                reverse('admin:add_scoreOne_one', args=[obj.pk]),
            )

    increase_score_one.short_description = 'Increase Score'
    increase_score_one.allow_tags = True

    def increase_score_two(self, obj):
        if obj.type == 'بسکتبال':
            return format_html(
                '<a class="button" href="{}">Add 1</a>&nbsp;'
                '<a class="button" href="{}">Add 2</a>&nbsp;'
                '<a class="button" href="{}">Add 3</a>',
                reverse('admin:add_scoreTwo_one', args=[obj.pk]),
                reverse('admin:add_scoreTwo_two', args=[obj.pk]),
                reverse('admin:add_scoreTwo_three', args=[obj.pk])
            )
        elif obj.type == 'فوتبال':
            return format_html(
                '<a class="button" href="{}">Add 1</a>&nbsp;',
                reverse('admin:add_scoreTwo_one', args=[obj.pk]),
            )

    increase_score_two.short_description = 'Increase Score'
    increase_score_two.allow_tags = True

    def process_addOne_one(self, request, match_id, *args, **kwargs):
        return self.process_action_add(
            request=request,
            match_id=match_id,
            action_title='Add One ScoreOne',
        )

    def process_addOne_two(self, request, match_id, *args, **kwargs):
        return self.process_action_add(
            request=request,
            match_id=match_id,
            action_title='Add Two ScoreOne',
        )

    def process_addOne_three(self, request, match_id, *args, **kwargs):
        return self.process_action_add(
            request=request,
            match_id=match_id,
            action_title='Add Three ScoreOne',
        )

    def process_addTwo_one(self, request, match_id, *args, **kwargs):
        return self.process_action_add(
            request=request,
            match_id=match_id,
            action_title='Add One ScoreTwo',
        )

    def process_addTwo_two(self, request, match_id, *args, **kwargs):
        return self.process_action_add(
            request=request,
            match_id=match_id,
            action_title='Add Two ScoreTwo',
        )

    def process_addTwo_three(self, request, match_id, *args, **kwargs):
        return self.process_action_add(
            request=request,
            match_id=match_id,
            action_title='Add Three ScoreTwo',
        )

    def process_action_add(self, request, match_id, action_title):
        match = self.get_object(request, match_id)
        if action_title == 'Add One ScoreOne':
            match.score1 += 1
        if action_title == 'Add Two ScoreOne':
            match.score1 += 2
        if action_title == 'Add Three ScoreOne':
            match.score1 += 3
        if action_title == 'Add One ScoreTwo':
            match.score2 += 1
        if action_title == 'Add Two ScoreTwo':
            match.score2 += 2
        if action_title == 'Add Three ScoreTwo':
            match.score2 += 3
        match.save()
        return HttpResponseRedirect('/admin/SportsApp/match')


class CoachingStaffInline(admin.StackedInline):
    model = CoachingStaff


class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'type']
    list_filter = [TypeFilter]
    search_fields = ['name',]
    inlines = [CoachingStaffInline]


class CommentInline(admin.TabularInline):
    model = Comment


class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'type', 'date']
    list_filter = ['date', TypeFilter]
    inlines = [CommentInline]


class PlayerStatsAdmin(admin.ModelAdmin):
    list_display = ['player_name', 'season', 'name', 'value', 'event_actions']
    search_fields = ['player_season__player__name', 'player_season__season']

    def player_name(self, obj):
        return obj.player_season.player.name

    def season(self, obj):
        return obj.player_season.season

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            url(
                r'^(?P<player_stat_id>.+)/add_event/$',
                self.admin_site.admin_view(self.process_event),
                name='add_value',
            ),
        ]
        return custom_urls + urls

    def event_actions(self, obj):
        return format_html(
            '<a class="button" href="{}">Add Value</a>&nbsp;',
            reverse('admin:add_value', args=[obj.pk]),
        )

    event_actions.short_description = 'Add Value'
    event_actions.allow_tags = True

    def process_event(self, request, player_stat_id, *args, **kwargs):
        return self.process_action(
            request=request,
            player_stat_id=player_stat_id,
            action_title='Add Value',
        )

    def process_action(self, request, player_stat_id, action_title):
        player_stat = self.get_object(request, player_stat_id)
        player_stat.value += 1
        player_stat.save()
        return HttpResponseRedirect('/admin/SportsApp/playerstat')


class LeagueAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'is_ongoing', 'start_date']
    list_filter = ['start_date', 'is_ongoing']


class PlayerStatsInline(admin.TabularInline):
    model = PlayerStat


class PlayerSeasonAdmin(admin.ModelAdmin):
    list_display = ['player', 'season']
    search_fields = ['player__name']
    inlines = [PlayerStatsInline,]


class MatchStatAdmin(admin.ModelAdmin):
    list_display = ['name', 'match_team1_name', 'first', 'event_actions_first', 'match_team2_name', 'second', 'event_actions_second']
    search_fields = ['match__team1__name', 'match__team2__name', 'name']
    list_filter = ['match__date']

    def match_team1_name(self, obj):
        return obj.match.team1.name

    def match_team2_name(self, obj):
        return obj.match.team2.name

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            url(
                r'^(?P<match_stat_id>.+)/add_first/$',
                self.admin_site.admin_view(self.process_event_first),
                name='add_first',
            ),
            url(
                r'^(?P<match_stat_id>.+)/add_second/$',
                self.admin_site.admin_view(self.process_event_second),
                name='add_second',
            ),
        ]
        return custom_urls + urls

    def event_actions_first(self, obj):
        return format_html(
            '<a class="button" href="{}">Add</a>',
            reverse('admin:add_first', args=[obj.pk]),
        )

    event_actions_first.short_description = 'Add'
    event_actions_first.allow_tags = True

    def event_actions_second(self, obj):
        return format_html(
            '<a class="button" href="{}">Add</a>',
            reverse('admin:add_second', args=[obj.pk]),
        )

    event_actions_second.short_description = 'Add'
    event_actions_second.allow_tags = True

    def process_event_first(self, request, match_stat_id, *args, **kwargs):
        return self.process_action(
            request=request,
            match_stat_id=match_stat_id,
            action_title='Add First',
        )

    def process_event_second(self, request, match_stat_id, *args, **kwargs):
        return self.process_action(
            request=request,
            match_stat_id=match_stat_id,
            action_title='Add Second',
        )

    def process_action(self, request, match_stat_id, action_title):
        match_stat = self.get_object(request, match_stat_id)
        if action_title == 'Add First':
            match_stat.first += 1
            match_stat.save()
        elif action_title == 'Add Second':
            match_stat.second += 1
            match_stat.save()
        return HttpResponseRedirect('/admin/SportsApp/matchstats')


class PlayerAdmin(admin.ModelAdmin):
    list_display = ['name', 'age', 'height', 'weight', 'nationality', 'teams']

    def teams(self, obj):
        team_positions = TeamPosition.objects.filter(player=obj)
        teams = []
        for t in team_positions:
            teams.append(t.team.name)
        return teams


class TeamPositionsAdmin(admin.ModelAdmin):
    list_display = ['team', 'player', 'position']
    search_fields = ['team__name', 'player__name', 'position']


class UserFollowPlayerAdmin(admin.ModelAdmin):
    list_display = ['user', 'player']
    search_fields = ['player__name']


class UserFollowTeamAdmin(admin.ModelAdmin):
    list_display = ['user', 'team']
    search_fields = ['team__name']


class MatchEventAdmin(admin.ModelAdmin):
    list_display = ['match', 'title', 'comment', 'time']
    list_filter = ['time']

admin.site.register(Tag)
admin.site.register(NewsArticle, NewsArticleAdmin)
admin.site.register(Comment)
admin.site.register(Player, PlayerAdmin)
admin.site.register(TeamPosition, TeamPositionsAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(League, LeagueAdmin)
admin.site.register(CoachingStaff)
admin.site.register(Match, MatchAdmin)
admin.site.register(MatchEvent, MatchEventAdmin)
admin.site.register(MatchStats, MatchStatAdmin)
admin.site.register(UserFollowTeam, UserFollowTeamAdmin)
admin.site.register(UserFollowPlayer, UserFollowPlayerAdmin)
admin.site.register(PlayerSeason, PlayerSeasonAdmin)
admin.site.register(PlayerStat, PlayerStatsAdmin)
