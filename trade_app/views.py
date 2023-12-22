from django.shortcuts import render
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
        lid = request.POST['lid']
        year = request.POST['year']
        data = league_setup(s2, sw, lid, year)
        league = AppLeague(id=lid, year=year, s2=s2, sw=sw, name=data['settings']['name'])
        league.save()
        for team in data.teams:
            t = Team(league=league.id, id=team['id'], name=team['name'])
            t.save()
        return HttpResponseRedirect(reverse("trade_app:index"))

    else:
        return render(request, "trade_app/index.html")

def roster(request, team_id):
    context = {"team_id": team_id}
    return render(request, "trade_app/roster.html", context)

def trade_form(request):
    return render(request, "trade_app/trade_form.html")