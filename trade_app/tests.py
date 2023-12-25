from django.test import TestCase
from .models import League as AppLeague, Team, Player, StatCard

# Create your tests here.
class LeagueTestCase(TestCase):
    def setUp(self):
        AppLeague.objects.create(name="League 1", year=2024, id=10, s2='abcdefgh', sw='ijklmnopqrs')

    def test_league_exists(self):
        l = AppLeague.objects.get(name="League 1")
        self.assertIsNotNone(l)
    