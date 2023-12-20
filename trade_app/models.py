from django.db import models

# Create your models here.
class League(models.Model):

    name = models.CharField(max_length=50)
    year = models.IntegerField()
    id = models.IntegerField()


class Team(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    id = models.IntegerField()



class Player(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

class PlayerStatCard(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)

class LeagueStatCard(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE)