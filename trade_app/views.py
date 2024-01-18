from typing import Any
from django.db.models import Max, F
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.template.defaulttags import register
from .helpers import league_setup, new_stat_card, new_empty_stat_card
import pandas as pd

from .models import League as AppLeague, Team, Player, StatCard
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def round_stat(num):
    if num:
        return str(round(num, 2))[:6]
    else:
        return 0.00

@register.filter
def stat_dict(stats):
    if stats:
        return stats.__dict__
    else:
        return None
    
KEYS = {'pts' : 'PTS', 'blk' : "BLK", "ast": 'AST', 'stl': 'STL', 
                           'oreb' : 'OREB', 'dreb': 'DREB', 'ftm': 'FTM', 'm3p': '3PM',
                            'afg' : 'AFG%', 'ato' : 'A/TO', 'ft_per' : 'FT%' }

# Create your views here.
def index(request):
    if request.method == 'POST':
        sw = request.POST['sw']
        s2 = request.POST['s2']
        lid = int(request.POST['lid'])
        year = int(request.POST['year'])
        data = league_setup(s2, sw, lid, year)
        league, _ = AppLeague.objects.update_or_create(id=lid, defaults={'year': year, 's2': s2, 'sw': sw, 
                                                                             'name': 'League(%s, %s)' % (data.league_id, data.year,)})
        league.create_teams(data.teams)
        for team in data.teams:
            t = Team.objects.get(pk=team.team_id)
            t.create_players(team.roster)
            t.create_team_statcard()
        league.create_league_statcard()
        league.save()
        return HttpResponseRedirect(reverse("trade_app:league", args=(league.id,)))

    else:
        return render(request, "trade_app/index.html")
    
class LeagueView(generic.DetailView):
    model = AppLeague
    template_name = 'trade_app/teams.html'
    context_object_name = 'league'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stats'] = self.object.statcard_set.first().__dict__
        context['keys'] = KEYS
        return context

class RosterView(generic.DetailView):
    model = Team
    template_name = 'trade_app/roster.html'
    context_object_name = 'team'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stats'] = self.object.statcard_set.first().__dict__
        context['keys'] = KEYS
        context['players'] = self.object.player_set.all().annotate(high_pts=Max('statcard__pts')).order_by(F('high_pts').desc(nulls_last=True))
        return context
    
class PlayerView(generic.DetailView):
    model = Player
    template_name = 'trade_app/player.html'
    context_object_name = 'player'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object.statcard_set.first():
            context['stats'] = self.object.statcard_set.first().__dict__
        else:
            context['stats'] = None
        context['keys'] = KEYS
        return context

def trade_form(request, pk):
    if request.method == 'POST':
        t1 = int(request.POST['self_team'])
        t2 = int(request.POST['other_team'])
        return HttpResponseRedirect(reverse("trade_app:player_trade_form", args=(t1, t2,)))
    
    else:
        league = get_object_or_404(AppLeague, pk=pk)
        context = { 'teams' : league.team_set.all(), 'id' : league.id}
        return render(request, "trade_app/trade_form.html", context)

def player_trade_form(request, t1, t2):
    if request.method == 'POST':
        give = []
        get = []
        for key, value in request.POST.items():
            if key.startswith('trading'):
                give.append(int(value))
            elif key.startswith('getting'):
                get.append(int(value))

        return HttpResponseRedirect(reverse("trade_app:trade_results", args=(give, get,)))
    
    else:
        team1 = get_object_or_404(Team, pk=t1)
        team2 = get_object_or_404(Team, pk=t2)
        stats1 = team1.statcard_set.first().__dict__
        stats2 = team1.statcard_set.first().__dict__
        players1 = team1.player_set.all().annotate(high_pts=Max('statcard__pts')).order_by(F('high_pts').desc(nulls_last=True))
        players2 = team2.player_set.all().annotate(high_pts=Max('statcard__pts')).order_by(F('high_pts').desc(nulls_last=True))
        context = { 'team1' : team1, 'team2' : team2, 'keys': KEYS, 'stats1' : stats1, 'stats2': stats2, 'players1': players1, 'players2' : players2}
        return render(request, "trade_app/player_trade_form.html", context)

def trade_results(request, give, get):
    get = get[1:-1].split(', ')
    give = give[1:-1].split(', ')
    getting_card = new_empty_stat_card(StatCard.objects)
    giving_card = new_empty_stat_card(StatCard.objects)
    getting_cards = {}
    giving_cards = {}
    
    for id in get:
        card = Player.objects.get(pk=int(id)).statcard_set.first()
        if card:
            getting_cards[card.player.name] = card.__dict__
        else:
            card = new_empty_stat_card(StatCard.objects)
            getting_cards[Player.objects.get(pk=int(id)).name] = card.__dict__
        new_stat_card(getting_card, card)
        card.delete()
        getting_card.get_calculated_stats()

    for id in give:
        card = Player.objects.get(pk=int(id)).statcard_set.first()
        if card:
            giving_cards[card.player.name] = card.__dict__
        else:
            card = new_empty_stat_card(StatCard.objects)
            giving_cards[Player.objects.get(pk=int(id)).name] = card.__dict__
        new_stat_card(giving_card, card)
        card.delete()
        giving_card.get_calculated_stats()

    getting_card_dict = getting_card.__dict__
    giving_card_dict = giving_card.__dict__
    getting_card.delete()
    giving_card.delete()

    for key in KEYS:
        getting_card_dict[key] -= giving_card_dict[key]

    context = {'card' : getting_card_dict, 'keys': KEYS, 'getting_cards' : getting_cards, 
               'giving_cards' : giving_cards}
    return render(request, "trade_app/trade_results.html", context)