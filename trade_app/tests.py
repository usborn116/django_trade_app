from django.test import TestCase
from .models import League as AppLeague, Team, Player, StatCard
from .test_data import fake_league, fake_team
from .helpers import league_setup, new_empty_stat_card

# Create your tests here.

sw = '{817F7C41-C9C5-43F7-BF7C-41C9C5F3F7EB}'
s2 = 'AEBZYDetmiWDzCsv91y%2B2bmAqE7WWTx2uT8JhJOE7pLZMjjQLcEt7DrPCRAqVyq0fiMyckLFBdJC1uID0R37CIaMmkghHDG62VAYnNAf7kVimrJfpf4KFUDm97dHy1NUa2TstxStusNhXVIbZbnVuuuKCRbdbQBDNyVRk9AW6Z0I%2FZIIwOFmStwPerqIiDejDTib94305LWGdRW7CLTcZwcmqtxGvOcq7hGOqYi26CdIPtzNSyEVfwlpdNg0dQuMyYzO%2Fw4w6h%2Fuh2OVah59Rw5DVajg%2FDvGZX9xNTiXTTdCow%3D%3D'
lid	= 780758162
year = 2024
data = league_setup(s2, sw, lid, year)

class LeagueTestCase(TestCase):
    def setUp(self):
        AppLeague.objects.create(name='League(%s, %s)' % (fake_league.league_id, fake_league.year,), 
                                 year=2024, id=10, s2='abcdefgh', sw='ijklmnopqrs')
        AppLeague.objects.create(id=lid, year=year, s2=s2, sw=sw, name='League(%s, %s)' % (data.league_id, data.year,))
    def test_league_exists(self):
        l = AppLeague.objects.get(name="League(10, 2024)")
        self.assertIsNotNone(l)
        l.create_teams(fake_league.teams)
        t = l.team_set.last()
        self.assertEqual(t.name, 'Test Team 2')

    def test_league_from_api(self):
        league = AppLeague.objects.get(pk=lid)
        self.assertEqual(league.name, 'League(780758162, 2024)')

class TeamTestCase(TestCase):
    def setUp(self):
        l = AppLeague.objects.create(name=fake_league['settings']['name'], 
                                 year=2024, id=10, s2='abcdefgh', sw='ijklmnopqrs')
        AppLeague.objects.create(id=lid, year=year, s2=s2, sw=sw, name='League(%s, %s)' % (data.league_id, data.year,))
        l.create_teams(fake_league.teams)
    
    def test_team_exists(self):
        t = Team.objects.get(name="Test Team")
        self.assertIsNotNone(t)

    def test_api_team_exists(self):
        league = AppLeague.objects.get(pk=lid)
        league.create_teams(data.teams)
        self.assertEqual(len(league.team_set.all()), 12)
        self.assertEqual(league.team_set.first().name, 'Paper Towns')

class PlayerTestCase(TestCase):
    def setUp(self):
        AppLeague.objects.create(id=lid, year=year, s2=s2, sw=sw, name='League(%s, %s)' % (data.league_id, data.year,))
        l = AppLeague.objects.create(name=fake_league['settings']['name'], 
                                 year=2024, id=10, s2='abcdefgh', sw='ijklmnopqrs')
        t = Team.objects.create(league=l, id=fake_team.team_id, name=fake_team.team_name)
        for player in fake_team.roster:
            Player.objects.create(league=l, team=t, name=player.name, position=player.position,
                                  id=player.playerId )

    def test_player_exists(self):
        p = Player.objects.get(name='Test Player Name')
        self.assertIsNotNone(p)

    def test_api_player_exists(self):
        league = AppLeague.objects.get(pk=lid)
        league.create_teams(data.teams)
        for team in data.teams:
            t = Team.objects.get(pk=team.team_id)
            t.create_players(team.roster)

        p = Player.objects.get(name='Kevin Durant')
        self.assertIsNotNone(p)
        self.assertEqual(p.team.name, 'SGA Holes')

class StatCardTestCase(TestCase):
    def setUp(self):
        league = AppLeague.objects.create(id=lid, year=year, s2=s2, sw=sw, name='League(%s, %s)' % (data.league_id, data.year,))
        league.create_teams(data.teams)
        for team in data.teams:
            t = Team.objects.get(pk=team.team_id)
            t.create_players(team.roster)
            t.create_team_statcard()

        league.create_league_statcard()

        l = AppLeague.objects.create(name=fake_league['settings']['name'], 
                                 year=2024, id=10, s2='abcdefgh', sw='ijklmnopqrs')
        l.create_teams(fake_league.teams)

        for team in fake_league.teams:
            t = Team.objects.get(pk=team.team_id)
            t.create_players(team.roster)
            t.create_team_statcard()

        l.create_league_statcard()

    def test_empty_card_generator(self):
        empt = new_empty_stat_card()
        self.assertEqual(empt.pts, 0.0)

    def test_player_statcard_exists(self):
        player_sc = StatCard.objects.get(player=Player.objects.get(pk=11))
        player_sc2 = StatCard.objects.get(player=Player.objects.get(pk=12))
        self.assertEqual(player_sc.pts, 15.0)
        self.assertEqual(player_sc2.pts, 5.0)
        self.assertEqual(player_sc.blk, 1.0)
        self.assertEqual(player_sc2.blk, 3.0)
        self.assertAlmostEqual(player_sc.afg, 0.835)
        self.assertAlmostEqual(player_sc.ato, 3.0)
        self.assertAlmostEqual(player_sc.ft_per, 0.9)
        self.assertAlmostEqual(player_sc2.afg, 0.615)
        self.assertAlmostEqual(player_sc2.ato, 2.0)
        self.assertAlmostEqual(player_sc2.ft_per, 0.8)

    def test_api_player_statcard_exists(self):
        player_sc = StatCard.objects.get(player=Player.objects.get(name='Kevin Durant'))
        self.assertIsNotNone(player_sc)

    def test_team_statcard_exists(self):
        team_sc = StatCard.objects.get(team=Team.objects.get(pk=100))
        team_sc2 = StatCard.objects.get(team=Team.objects.get(pk=900))
        self.assertAlmostEqual(team_sc.pts, 20.0)
        self.assertAlmostEqual(team_sc2.pts, 5.0)
        self.assertAlmostEqual(team_sc.blk, 4.0)
        self.assertAlmostEqual(team_sc2.blk, 3.0)
        self.assertAlmostEqual(team_sc.afg, 0.725)
        self.assertAlmostEqual(team_sc.ato, 2.6666667)
        self.assertAlmostEqual(team_sc.ft_per, 0.85)
        self.assertAlmostEqual(team_sc2.afg, 0.6125)
        self.assertAlmostEqual(team_sc2.ato, 1.75)
        self.assertAlmostEqual(team_sc2.ft_per, 0.675)

    def test_api_team_statcard_exists(self):
        team_sc = StatCard.objects.get(team=Team.objects.get(name='SGA Holes'))
        self.assertIsNotNone(team_sc)

    def test_league_statcard_exists(self):
        league_sc = StatCard.objects.get(league=AppLeague.objects.get(pk=10))
        self.assertAlmostEqual(league_sc.pts, 12.5)
        self.assertAlmostEqual(league_sc.blk, 3.5)
        self.assertAlmostEqual(league_sc.ast, 7.5)
        # (15 * .5 + 260) / 400
        self.assertAlmostEqual(league_sc.afg, 0.66875)
        # 7.5 / 3.5
        self.assertAlmostEqual(league_sc.ato, 2.14285714)
        self.assertAlmostEqual(league_sc.ft_per, 0.7625)

    def test_api_league_statcard_exists(self):
        league_sc = StatCard.objects.get(league=AppLeague.objects.get(pk=lid))
        self.assertIsNotNone(league_sc)