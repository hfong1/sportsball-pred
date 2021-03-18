from django.db import models


# Create your models here.
class TeamID(models.Model):
    team_id = models.IntegerField(unique=True)
    team_name = models.CharField(max_length=100)

