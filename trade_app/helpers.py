from espn_api.basketball import League
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

def stat_card_diff(new_stat, card):
    if card:
        new_stat.pts -= card.pts
        new_stat.blk -= card.blk
        new_stat.stl -= card.stl
        new_stat.ast -= card.ast
        new_stat.oreb -= card.oreb
        new_stat.dreb -= card.dreb
        new_stat.to -= card.to
        new_stat.fga -= card.fga
        new_stat.fgm -= card.fgm
        new_stat.ftm -= card.ftm
        new_stat.fta -= card.fta
        new_stat.m3p -= card.m3p
        new_stat.a3p -= card.a3p
        new_stat.save()