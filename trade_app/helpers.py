from espn_api.basketball import League
from .models import StatCard
import pandas as pd

def league_setup(s2,sw,lid,lyear):
    return League(league_id=lid, year=lyear, espn_s2 = s2, swid = sw)

def new_stat_card(new_stat, card):
    if card:
        new_stat.pts += card.pts
        new_stat.blk += card.blk
        new_stat.stl += card.stl
        new_stat.ast += card.ast
        new_stat.oreb += card.oreb
        new_stat.dreb += card.dreb
        new_stat.to += card.to
        new_stat.fga += card.fga
        new_stat.fgm += card.fgm
        new_stat.ftm += card.ftm
        new_stat.fta += card.fta
        new_stat.m3p += card.m3p
        new_stat.a3p += card.a3p
        new_stat.save()

def new_empty_stat_card(owner = StatCard.objects):
    card = owner.create(pts=0.0, blk=0.0, stl=0.0, ast=0.0, oreb=0.0, dreb=0.0, to=0.0, 
                                    fga=0.0, fgm=0.0, ftm=0.0, fta=0.0, m3p=0.0, a3p=0.0)
    card.save()
    return card