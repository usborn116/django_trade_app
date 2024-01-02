from django.test import TestCase
from .models import League as AppLeague, Team, Player, StatCard
from .test_data import fake_league, fake_team, fake_player, fake_team_2

# Create your tests here.

class LeagueTestCase(TestCase):
    def setUp(self):
        AppLeague.objects.create(name=fake_league['settings']['name'], 
                                 year=2024, id=10, s2='abcdefgh', sw='ijklmnopqrs')
    def test_league_exists(self):
        l = AppLeague.objects.get(name="Test League")
        self.assertIsNotNone(l)
        l.create_teams([fake_team])
        t = l.team_set.first()
        self.assertEqual(t.name, 'Test Team')
        t.create_players([fake_player])
        p = t.player_set.first()
        self.assertEqual(p.name, 'Test Player Name')

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
        l.create_teams(fake_league['teams'])
        t = Team.objects.first()
        t2 = Team.objects.last()
        t.create_players(fake_team['roster'])
        t2.create_players(fake_team_2['roster'])
        t.create_team_statcard()
        t2.create_team_statcard()
        l.create_league_statcard()

    def test_player_statcard_exists(self):
        player_sc = StatCard.objects.all()[0]
        player_sc2 = StatCard.objects.all()[1]
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
        

    def test_team_statcard_exists(self):
        team_sc = StatCard.objects.all()[4]
        team_sc2 = StatCard.objects.all()[5]
        self.assertAlmostEqual(team_sc.pts, 10.0)
        self.assertAlmostEqual(team_sc2.pts, 2.5)
        self.assertAlmostEqual(team_sc.blk, 2.0)
        self.assertAlmostEqual(team_sc2.blk, 1.5)
        self.assertAlmostEqual(team_sc.afg, 0.725)
        self.assertAlmostEqual(team_sc.ato, 2.6666667)
        self.assertAlmostEqual(team_sc.ft_per, 0.85)
        self.assertAlmostEqual(team_sc2.afg, 0.6125)
        self.assertAlmostEqual(team_sc2.ato, 1.75)
        self.assertAlmostEqual(team_sc2.ft_per, 0.675)

    def test_team_statcard_exists(self):
        league_sc = StatCard.objects.all()[6]
        self.assertAlmostEqual(league_sc.pts, 6.25)
        self.assertAlmostEqual(league_sc.blk, 1.75)
        self.assertAlmostEqual(league_sc.ast, 3.75)

        # (15 * .5 + 260) / 400
        self.assertAlmostEqual(league_sc.afg, 0.66875)

        # 7.5 / 3.5
        self.assertAlmostEqual(league_sc.ato, 2.14285714)
        self.assertAlmostEqual(league_sc.ft_per, 0.7625)
    