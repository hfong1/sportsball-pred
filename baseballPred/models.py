from django.db import models


# Create your models here.
class TeamID(models.Model):
    team_id = models.IntegerField(unique=True)
    team_name = models.CharField(max_length=100)


class GameBetweenTeams(models.Model):
    game_id = models.IntegerField(primary_key=True, unique=True)
    game_datetime = models.DateTimeField()
    game_date = models.DateField()
    game_type = models.CharField(max_length=30)
    status = models.CharField(max_length=30)
    away_name = models.CharField(max_length=30)
    home_name = models.CharField(max_length=30)
    away_id = models.IntegerField()
    home_id = models.IntegerField()
    doubleheader = models.CharField(max_length=30)
    game_num = models.IntegerField()
    home_probable_pitcher = models.CharField(max_length=30)
    away_probable_pitcher = models.CharField(max_length=30)
    home_pitcher_note = models.CharField(max_length=256)
    away_pitcher_note = models.CharField(max_length=256)
    away_score = models.IntegerField()
    home_score = models.IntegerField()
    current_inning = models.IntegerField(null=True)
    inning_state = models.CharField(max_length=30)
    venue_id = models.IntegerField()
    venue_name = models.CharField(max_length=30)
    winning_team = models.CharField(max_length=30)
    losing_team = models.CharField(max_length=30)
    winning_pitcher = models.CharField(max_length=30)
    losing_pitcher = models.CharField(max_length=30)
    save_pitcher = models.CharField(max_length=30, null=True, blank=True)
    summary = models.CharField(max_length=256)


class GamesBetweenTeamsHistory(models.Model):
    team1_id = models.IntegerField()
    team2_id = models.IntegerField()
    game_id = models.OneToOneField(GameBetweenTeams, on_delete=models.CASCADE)
