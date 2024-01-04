from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.template.defaulttags import register
from .helpers import league_setup
import pandas as pd

from .models import League as AppLeague, Team, Player, StatCard
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def round_stat(num):
    return round(num, 2)

# Create your views here.
def index(request):
    if request.method == 'POST':
        sw = request.POST['sw']
        s2 = request.POST['s2']
        lid = int(request.POST['lid'])
        year = int(request.POST['year'])
        data = league_setup(s2, sw, lid, year)
        league, _ = AppLeague.objects.get_or_create(id=lid, year=year, s2=s2, sw=sw, 
                                                          name='League(%s, %s)' % (data.league_id, data.year,))
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
        context['keys'] = {'pts' : 'PTS', 'blk' : "BLK", "ast": 'AST', 'stl': 'STL', 
                           'oreb' : 'OREB', 'dreb': 'DREB', 'ftm': 'FTM', 'm3p': '3PM',
                            'afg' : 'AFG%', 'ato' : 'A/TO', 'ft_per' : 'FT%' }
        return context

class RosterView(generic.DetailView):
    model = Team
    template_name = 'trade_app/roster.html'
    context_object_name = 'team'
'''
def roster(request, team_id):
    context = {"team_id": team_id}
    return render(request, "trade_app/roster.html", context)
''' 
def trade_form(request):
    return render(request, "trade_app/trade_form.html")