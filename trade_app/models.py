from django.db import models
from .helpers import new_stat_card, update_stat_card, new_empty_stat_card

# Create your models here.
class League(models.Model):
    name = models.CharField(max_length=50)
    year = models.IntegerField()
    id = models.IntegerField(primary_key=True)
    s2 = models.CharField(max_length=2000, default=None)
    sw = models.CharField(max_length=2000, default=None)

    def create_league_statcard(self):
        new_stat = None
        temp_card = new_empty_stat_card(StatCard.objects)
        for team in self.team_set.all():
                for card in team.statcard_set.all():
                    new_stat_card(temp_card, card)
        if not self.statcard_set.first():
            new_stat = new_empty_stat_card(self.statcard_set)
            new_stat_card(new_stat, temp_card)
        else:
            new_stat = self.statcard_set.first()
            update_stat_card(new_stat, temp_card)

        new_stat.get_averages(len(self.team_set.all()))

    def create_teams(self, teams):
        for team in teams:
            Team.objects.update_or_create(id = team.team_id, defaults={'name' : team.team_name, 'league' : self})


class Team(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    id = models.IntegerField(primary_key=True)

    def create_players(self, players):
        for player in players:
            new_player, _ = Player.objects.update_or_create(id = player.playerId, defaults={'name' : player.name, 'league' : self.league,
                                   'position':player.position, 'team' : self})
            try:
                new_player.create_player_statcard(player.stats['2024_total']['avg'])
            except KeyError:
                None
            
    def create_team_statcard(self):
        new_stat = None
        temp_card = new_empty_stat_card(StatCard.objects)

        for player in self.player_set.all():
                for card in player.statcard_set.all():
                    new_stat_card(temp_card, card)

        if not self.statcard_set.first():
            new_stat = new_empty_stat_card(self.statcard_set)
            new_stat_card(new_stat, temp_card)
        else:
            new_stat = self.statcard_set.first()
            update_stat_card(new_stat, temp_card)

        temp_card.delete()
        new_stat.get_calculated_stats()
        new_stat.save()
                
class Player(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    id = models.IntegerField(primary_key=True)
    position = models.CharField(max_length=10)
    ordering = ['statcard__pts']
    def create_player_statcard(self, stats):
        new_stat = None
        temp_card = StatCard.objects.create(pts=stats['PTS'], blk=stats['BLK'], stl=stats['STL'], 
                                    ast=stats['AST'], oreb=stats['OREB'], dreb=stats['DREB'], to=stats['TO'], 
                                    fga=stats['FGA'], fgm=stats['FGM'], ftm=stats['FTM'], fta=stats['FTA'], 
                                    m3p=stats['3PTM'], a3p=stats['3PTA'])
        if not self.statcard_set.first():
            new_stat = new_empty_stat_card(self.statcard_set)
            new_stat_card(new_stat, temp_card)
        else:
            new_stat = self.statcard_set.first()
            update_stat_card(new_stat, temp_card)
        
        temp_card.delete()
        new_stat.get_calculated_stats()
        new_stat.save()

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

    ordering = ['pts']

    def get_calculated_stats(self):
        self.afg = (self.m3p*0.5+self.fgm) / (self.fga + 0.0000000001)
        self.ato = self.ast / (self.to + 0.00000000001)
        self.ft_per = self.ftm / (self.fta + 0.0000000001)

    def get_averages(self, divisor):
        self.pts = self.pts/divisor
        self.blk = self.blk/divisor
        self.stl = self.stl/divisor
        self.ast = self.ast/divisor
        self.oreb = self.oreb/divisor
        self.dreb = self.dreb/divisor
        self.to = self.to/divisor
        self.get_calculated_stats()
        self.save()