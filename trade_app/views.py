from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .helpers import league_setup
import pandas as pd

from .models import League as AppLeague, Team, Player, StatCard

# Create your views here.
def index(request):
    if request.method == 'POST':
        sw = request.POST['sw']
        s2 = request.POST['s2']
        lid = int(request.POST['lid'])
        year = int(request.POST['year'])
        data = league_setup(s2, sw, lid, year)
        league, created = AppLeague.objects.get_or_create(id=lid, year=year, s2=s2, sw=sw, 
                                                          name='League(%s, %s)' % (data.league_id, data.year,))
        league.save()
        league.create_teams(data.teams)
        return HttpResponseRedirect(reverse("trade_app:league", args=(league.id,)))

    else:
        return render(request, "trade_app/index.html")
    
def league(request, league_id):
    league = get_object_or_404(AppLeague, pk=league_id)
    context = {'teams' : league.team_set.all()}
    return render(request, "trade_app/teams.html", context)

def roster(request, team_id):
    context = {"team_id": team_id}
    return render(request, "trade_app/roster.html", context)

def trade_form(request):
    return render(request, "trade_app/trade_form.html")