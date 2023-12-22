from django.db import models

# Create your models here.
class League(models.Model):
    name = models.CharField(max_length=50)
    year = models.IntegerField()
    id = models.IntegerField(primary_key=True)
    s2: models.CharField(max_length=2000)
    sw: models.CharField(max_length=2000)


class Team(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    id = models.IntegerField(primary_key=True)

class Player(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    id = models.IntegerField(primary_key=True)
    position = models.CharField(max_length=10)

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
    afg = models.FloatField("AFG%")
    ato = models.FloatField("A/TO")
    ft_per = models.FloatField("FT%")