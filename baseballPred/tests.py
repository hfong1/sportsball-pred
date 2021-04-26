from django.test import TestCase
from baseballPred.GamesBetweenTeams import getGamesBetweenTeams
from baseballPred.BNET import get_bn_winrate
from baseballPred.models import GameBetweenTeams, GamesBetweenTeamsHistory
from django.forms.models import model_to_dict


# Create your tests here.
class DatabaseApiTests(TestCase):
    def setup(self):
        test = getGamesBetweenTeams(143, 120, '01/01/2015', '12/31/2019')

    # check IDs of games to see if they're inserted properly into the database
    def test_db_insertion_games_between_teams(self):
        game_ids = GamesBetweenTeamsHistory.objects \
            .filter(team1_id=143, team2_id=120) \
            .order_by('game_id')

        games = [model_to_dict(game.game_id) for game in game_ids]
        games_ids_list = [game['game_id'] for game in games]

        # expected inserted ids
        inserted_game_ids = [
            565898, 565899, 565929, 565930,
            565931, 565932, 565969, 565970,
            565971, 565972, 567065, 567066,
            567067, 567077, 567078, 567079,
            567103, 567104, 567105, 630853,
            630855, 630884, 630888, 630892,
            630896, 631143, 631145, 631146,
            631153,
        ]

        self.assertEqual(games_ids_list, inserted_game_ids)
        self.assertEqual(len(games), 29)

    # check if winrates are expected winrates
    def test_get_winrate(self):
        test = getGamesBetweenTeams(143, 120, '01/01/2015', '12/31/2019')
        winrate = test.getWinRate()
        winrate = round(float(winrate), 5)

        bn_winrate = round(get_bn_winrate(test, 5, 5), 5)

        self.assertEqual(winrate, .38095)
        self.assertEqual(bn_winrate, .47154)
