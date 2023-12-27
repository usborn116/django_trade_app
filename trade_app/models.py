from django.db import models

# Create your models here.
class League(models.Model):
    name = models.CharField(max_length=50)
    year = models.IntegerField()
    id = models.IntegerField(primary_key=True)
    s2 = models.CharField(max_length=2000, default=None)
    sw = models.CharField(max_length=2000, default=None)

    #def create_league_statcard(self):


class Team(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    id = models.IntegerField(primary_key=True)

    #def create_team_statcard(self):

class Player(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    id = models.IntegerField(primary_key=True)
    position = models.CharField(max_length=10)

    #def create_player_statcard(self):

class StatCard(models.Model):
    player = models.ForeignKey(Player, blank=True, null=True, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, blank=True, null=True, on_delete=models.CASCADE)
    league = models.ForeignKey(League, blank=True, null=True, on_delete=models.CASCADE)
    pts = models.FloatField()
    blk = models.FloatField()
    stl = models.FloatField()
    ast = models.FloatField()
    oreb = models.FloatField()
    dreb = models.FloatField()
    to = models.FloatField()
    fga = models.FloatField()
    fgm = models.FloatField()
    ftm = models.FloatField()
    fta = models.FloatField()
    m3p = models.FloatField("3PTM")
    a3p = models.FloatField("3PTA")
    afg = models.FloatField("AFG%", blank=True, null=True)
    ato = models.FloatField("A/TO", blank=True, null=True,)
    ft_per = models.FloatField("FT%", blank=True, null=True,)

    def get_calculated_stats(self):
        self.afg = (self.m3p*0.5+self.fgm) / self.fga
        self.ato = self.ast / self.to
        self.ft_per = self.ftm / self.fta