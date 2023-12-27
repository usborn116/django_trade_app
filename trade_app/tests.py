from django.test import TestCase
from .models import League as AppLeague, Team, Player, StatCard
from .test_data import fake_league, fake_team, fake_player

# Create your tests here.

class LeagueTestCase(TestCase):
    def setUp(self):
        AppLeague.objects.create(name=fake_league['settings']['name'], 
                                 year=2024, id=10, s2='abcdefgh', sw='ijklmnopqrs')
    def test_league_exists(self):
        l = AppLeague.objects.get(name="Test League")
        self.assertIsNotNone(l)

class TeamTestCase(TestCase):
    def setUp(self):
        l = AppLeague.objects.create(name=fake_league['settings']['name'], 
                                 year=2024, id=10, s2='abcdefgh', sw='ijklmnopqrs')
        Team.objects.create(league=l, id=fake_team['id'], name=fake_team['name'])
    
    def test_team_exists(self):
        t = Team.objects.get(name="Test Team")
        self.assertIsNotNone(t)

class PlayerTestCase(TestCase):
    def setUp(self):
        l = AppLeague.objects.create(name=fake_league['settings']['name'], 
                                 year=2024, id=10, s2='abcdefgh', sw='ijklmnopqrs')
        t = Team.objects.create(league=l, id=fake_team['id'], name=fake_team['name'])
        for player in fake_team['roster']:
            Player.objects.create(league=l, team=t, name=player['name'], position=player['position'],
                                  id=player['id'] )

    def test_player_exists(self):
        p = Player.objects.get(name='Test Player Name')
        self.assertIsNotNone(p)

class StatCardTestCase(TestCase):
    def setUp(self):
        l = AppLeague.objects.create(name=fake_league['settings']['name'], 
                                 year=2024, id=10, s2='abcdefgh', sw='ijklmnopqrs')
        t = Team.objects.create(league=l, id=fake_team['id'], name=fake_team['name'])
        p = Player.objects.create(league=l, team=t, name=fake_player['name'], position=fake_player['position'],
                                  id=fake_player['id'] )
        stats = fake_player['stats']['2024_total']['avg']
        StatCard.objects.create(player=p, pts=stats['PTS'], blk=stats['BLK'], stl=stats['STL'], 
                                ast=stats['AST'], oreb=stats['OREB'], dreb=stats['DREB'], to=stats['TO'], 
                                fga=stats['FGA'], fgm=stats['FGM'], ftm=stats['FTM'], fta=stats['FTA'], 
                                m3p=stats['3PTM'], a3p=stats['3PTA'])

    def test_player_statcard_exists(self):
        player_sc = StatCard.objects.first()
        self.assertIsNotNone(player_sc)
        player_sc.get_calculated_stats()
        self.assertEqual(player_sc.pts, 15.0)
        self.assertEqual(player_sc.blk, 1.0)
        self.assertEqual(player_sc.stl, 1.0)
        self.assertEqual(player_sc.ast, 6.0)
        self.assertAlmostEqual(player_sc.afg, 0.835)
        self.assertAlmostEqual(player_sc.ato, 3.0)
        self.assertAlmostEqual(player_sc.ft_per, 0.9)
        self.assertIsNotNone(player_sc.player)
        self.assertIsNone(player_sc.team)
        self.assertIsNone(player_sc.league)

    #def test_team_statcard_exists(self):
    