from espn_api.basketball import League
import pandas as pd

def league_setup(s2,sw,lid,lyear):
    return League(league_id=lid, year=lyear, espn_s2 = s2, swid = sw)