import statsapi
from datetime import date
from functools import reduce
import pandas as pd

# Heads up: Python-3 and 5 spaces as a tab.

# Something we need to decide is whether to build around team_id's or team names

# There's an option to make this developer friendly by wrapping dictionaries
#   into classes for safety nets in development... however with proper var
#   names, we won't make the mistake of plugging the wrong dict to the wrong func.
#   There is a cost of space and time to be concerned about, too.

# Ideally, we would have a dictionary reflecting team name -> team id but
#   that can be done at a later time. This dict will be expanded upon the
#   longer the run time in case you need to pull again.

# Given a Team Name, retrieve the team_id
# fill in the DICT with     print(statsapi.get('teams',{'sportsIds':1}))
team_id_dict = {
    # National League 
    'Arizona Diamondbacks':109,
    'Chicago Cubs': 112,
    'Cincinnati Reds': 113,
    'Colorado Rockies':115,
    'Los Angeles Dodgers':119,
    'Washington Nationals':120,
    'New York Mets':121,
    'Pittsburgh Pirates':134,
    'San Diego Padres':135,
    'San Francisco Giants':137,
    'St. Louis Cardinals':138,
    'Philadelphia Phillies':143,
    'Atlanta Braves':144,
    'Miami Marlins':146,
    'Milwaukee Brewers':158,
    # American League
    'Los Angeles Angels':108,
    'Baltimore Orioles':110,
    'Boston Red Sox':111,
    'Cleveland Indians':114,
    'Detroit Tigers':116,
    'Houston Astros':117,
    'Kansas City Royals':118,
    'Oakland Athletics':133,
    'Seattle Mariners':136,
    'Tampa Bay Rays':139,
    'Texas Rangers':140,
    'Toronto Blue Jays':141,
    'Minnesota Twins':142,
    'Chicago White Sox':145,
    'New York Yankees':147
}


# It is also possible to store the below class in a dict
#   to act as memory but we'll need a more final product
#   to actually discuss its feasibility.

# Ok I lied, we'll need a class for this specifically as we need
#   information automatically sorted by team1 and team2 for
#   simpler abstractions. This will probably be thrown out
#   in the future, but the overall structure will be used.

# A wrapper class for GamesBetweenTeam list.
class GamesBetweenTeams:
    team1_id = -1
    team2_id = -1
    team1 = ''
    team2 = ''
    games = []
    start_date = ''
    end_date = ''

    win_rate = -1

    # batting stats
    runs = [[],[]]
    doubles = [[],[]]
    triples = [[],[]]
    homeRuns = [[],[]]
    strikeOuts = [[],[]]
    baseOnBalls= [[],[]]
    hits = [[],[]]
    avg = [[],[]]
    atBats = [[],[]]
    obp = [[],[]]
    slg = [[],[]]

    record = []
    ops = [[],[]]

    stolenBases = [[],[]]
    leftOnBase = [[],[]]
    #pitching stats
    era = [[],[]]

    earnedRuns = [[],[]]

    # Given the id's of two teams, return create a class of games between team1
    #   and team2.
    # Head's up, the function in the module that calls this has default arguments
    #   but in case we choose to dissect this class for later, duplicate the two
    #   arguments.
    def __init__(self, team1_id, team2_id, start_date='input start mm/dd/YY', end_date='input end mm/dd/YY'):
        self.team1_id = team1_id
        self.team2_id = team2_id
 
        self.team1 = self.lookUpTeamName(self.team1_id)
        self.team2 = self.lookUpTeamName(self.team2_id)

        self.start_date = start_date
        if end_date == '':
            self.end_date = date.today().strftime('%m/%d/%Y')
        elif end_date != '':
            self.end_date = end_date

        # self.games = statsapi.schedule(start_date=start_date,end_date=end_date,team=team1_id,opponent=team2_id)
        # self.getInSeasonGames()   #only look at regular season games (non including preseason or playoff games)

        self.getAllGames()
        self.getInSeasonGames()
        print(len(self.games))

        # print(self.team1)
        # print(self.team1_id)
        # print(self.team2)
        # print(self.team2_id)

        # And the rest is the HTML

        # print(self.games)
        # print(statsapi.meta('gameTypes'))

    # Get the win rate simply by W/L
    def getWinRate(self):
        # This exists if in the future, we choose not to store win_rate.
        if self.win_rate != -1:
            return self.win_rate
        
        team1_wins = 0
        team1_losses = 0
        team1_ties = 0

        if len(self.games) == 0:
            return f"No games were played between the {self.team1} and the {self.team2}"
        # Traverse through games.
        for game in self.games:
            if game.get('winning_team') == self.team1:
                team1_wins += 1
            elif game.get('winning_team') == self.team2:
                team1_losses += 1
            elif game.get('status') == 'Final: Tied':
                team1_ties += 1

        # print(f"wins: {team1_wins}")
        # print(f"losses: {team1_losses}")
        # print(f"ties: {team1_ties}")
        
        # there will not be ties in regular season, or postseason, however if we decide to use pre season
        # then there are ties.
        # win rate is wins / total games... if there are ties, then it is the formula below.
        self.win_rate = (team1_wins + 0.5*team1_ties) / (team1_wins + team1_losses + team1_ties)
        return self.win_rate

    # I have doubts we'll ever use this but it exists if we need to use it
    #   to refresh contents of the table
    def refresh(self):
        self.win_rate = -1
        self.games = 'Add HTML call here'

    # Return the list of games.
    def getGames(self):
        return self.games

    def findSchedule(self, start_date, end_date):
        games = statsapi.schedule(start_date=start_date,end_date=end_date,team=self.team1_id,opponent=self.team2_id)
        return games

    # this funciton uses date and month, the other funciton will use just seasons to make it easier
    def getAllGames(self):
        start_y = int(self.start_date[6:10])
        end_y = int(self.end_date[6:10])

        SOY = f'01/01/{start_y}'
        EOY = f'12/31/{start_y}'

        if(start_y == end_y):
            self.games.append(self.findSchedule(self.start_date, self.end_date))
        elif(start_y < end_y):
            self.games.append(self.findSchedule(self.start_date, EOY))
            start_y += 1
            while(start_y < end_y):
                SOY = f'01/01/{start_y}'
                EOY = f'12/31/{start_y}'
                self.games.append(self.findSchedule(SOY, EOY))
                start_y += 1
            SOY = f'01/01/{start_y}'
            self.games.append(self.findSchedule(SOY, self.end_date))

        # print(start_m)
        # print(start_d)
        # print(start_y)
        # print(end_m)
        # print(end_d)
        # print(end_y)
    # right now this funciton will change the self.games to only be the games from the regular season
    def getInSeasonGames(self):
        season_games = []
        for season in self.games:
            for game in season:
                if (game.get('game_type') == 'R' and game.get('status') == 'Final'):      #if the game is a regular season game
                    season_games.append(game)

            self.games = season_games
        return
    
    # similar to getTeamIdFromNeamName except it gets the name from the id
    def lookUpTeamName(self, team_id):
        for key, value in team_id_dict.items():
            if team_id == value:
                return key
        return "DNE"        #does not exist

    def getStats(self):
        team1 = {
            'runs': self.runs[0],
            'doubles': self.doubles[0],
            'triples': self.triples[0],
            'homeRuns': self.homeRuns[0],
            'strikeOuts': self.strikeOuts[0],
            'baseOnBalls': self.baseOnBalls[0],
            'hits': self.hits[0],
            'avg': self.avg[0],
            'atBats': self.atBats[0],
            'obp': self.obp[0],
            'slg': self.slg[0],
            'record': self.record,
            'ops': self.ops[0],
            'stolenBases': self.stolenBases[0],
            'leftOnBase': self.leftOnBase[0],
            'era': self.era[0],
            'earnedRuns': self.earnedRuns[0],
        }
        team2 = {
            'runs': self.runs[1],
            'doubles': self.doubles[1],
            'triples': self.triples[1],
            'homeRuns': self.homeRuns[1],
            'strikeOuts': self.strikeOuts[1],
            'baseOnBalls': self.baseOnBalls[1],
            'hits': self.hits[1],
            'avg': self.avg[1],
            'atBats': self.atBats[1],
            'obp': self.obp[1],
            'slg': self.slg[1],
            'record': list(map(lambda x: 1 - x, self.record)),
            'ops': self.ops[1],
            'stolenBases': self.stolenBases[1],
            'leftOnBase': self.leftOnBase[1],
            'era': self.era[1],
            'earnedRuns': self.earnedRuns[1],
        }

        return team1, team2

    @staticmethod
    def average(lst):
        if isinstance(lst[0], str):
            lst = list(map(lambda x: float(x), lst))
        return round(reduce(lambda a, b: a + b, lst) / len(lst), 3)

    def getStatAverages(self):
        team1 = {
            'runs': self.average(self.runs[0]),
            'doubles': self.average(self.doubles[0]),
            'triples': self.average(self.triples[0]),
            'homeRuns': self.average(self.homeRuns[0]),
            'strikeOuts': self.average(self.strikeOuts[0]),
            'baseOnBalls': self.average(self.baseOnBalls[0]),
            'hits': self.average(self.hits[0]),
            'avg': self.average(self.avg[0]),
            'atBats': self.average(self.atBats[0]),
            'obp': self.average(self.obp[0]),
            'slg': self.average(self.slg[0]),
            'record': sum(self.record),
            'ops': self.average(self.ops[0]),
            'stolenBases': self.average(self.stolenBases[0]),
            'leftOnBase': self.average(self.leftOnBase[0]),
            'era': self.average(self.era[0]),
            'earnedRuns': self.average(self.earnedRuns[0]),
        }
        team2 = {
            'runs': self.average(self.runs[1]),
            'doubles': self.average(self.doubles[1]),
            'triples': self.average(self.triples[1]),
            'homeRuns': self.average(self.homeRuns[1]),
            'strikeOuts': self.average(self.strikeOuts[1]),
            'baseOnBalls': self.average(self.baseOnBalls[1]),
            'hits': self.average(self.hits[1]),
            'avg': self.average(self.avg[1]),
            'atBats': self.average(self.atBats[1]),
            'obp': self.average(self.obp[1]),
            'slg': self.average(self.slg[1]),
            'record': len(self.record) - sum(self.record),
            'ops': self.average(self.ops[1]),
            'stolenBases': self.average(self.stolenBases[1]),
            'leftOnBase': self.average(self.leftOnBase[1]),
            'era': self.average(self.era[1]),
            'earnedRuns': self.average(self.earnedRuns[1]),
        }

        return team1, team2

    # And the remaining structure would look something like this... for now.
    def setStats(self):
        # game = self.games[0]

        # game = statsapi.boxscore_data(game.get('game_id'))
        for game in self.games:
            if game.get('winning_team') == self.team1:
                self.record.append(1)
            elif game.get('winning_team') == self.team2:
                self.record.append(0)

            game = statsapi.boxscore_data(game.get('game_id'))
            away_batting = game.get('away').get('teamStats').get('batting')
            home_batting = game.get('home').get('teamStats').get('batting')
            away_pitching = game.get('away').get('teamStats').get('pitching')
            home_pitching = game.get('home').get('teamStats').get('pitching')
            if game.get('away').get('team').get('id') == self.team1_id:
                team1_idx = 0
                team2_idx = 1
            else:
                team1_idx = 1
                team2_idx = 0

            self.runs[team1_idx].append(away_batting.get('runs'))
            self.doubles[team1_idx].append(away_batting.get('doubles'))
            self.triples[team1_idx].append(away_batting.get('triples'))
            self.homeRuns[team1_idx].append(away_batting.get('homeRuns'))
            self.strikeOuts[team1_idx].append(away_batting.get('strikeOuts'))
            self.baseOnBalls[team1_idx].append(away_batting.get('baseOnBalls'))
            self.hits[team1_idx].append(away_batting.get('hits'))
            self.avg[team1_idx].append(away_batting.get('avg'))
            self.atBats[team1_idx].append(away_batting.get('atBats'))
            self.obp[team1_idx].append(away_batting.get('obp'))
            self.slg[team1_idx].append(away_batting.get('slg'))
            self.stolenBases[team1_idx].append(away_batting.get('stolenBases'))
            self.leftOnBase[team1_idx].append(away_batting.get('leftOnBase'))
            self.earnedRuns[team1_idx].append(away_pitching.get('earnedRuns'))

            self.ops[team1_idx].append(away_batting.get('ops'))  # ops statistics
            self.era[team1_idx].append(away_pitching.get('era'))  # era statistics

            self.runs[team2_idx].append(home_batting.get('runs'))
            self.doubles[team2_idx].append(home_batting.get('doubles'))
            self.triples[team2_idx].append(home_batting.get('triples'))
            self.homeRuns[team2_idx].append(home_batting.get('homeRuns'))
            self.strikeOuts[team2_idx].append(home_batting.get('strikeOuts'))
            self.baseOnBalls[team2_idx].append(home_batting.get('baseOnBalls'))
            self.hits[team2_idx].append(home_batting.get('hits'))
            self.avg[team2_idx].append(home_batting.get('avg'))
            self.atBats[team2_idx].append(home_batting.get('atBats'))
            self.obp[team2_idx].append(home_batting.get('obp'))
            self.slg[team2_idx].append(home_batting.get('slg'))
            self.stolenBases[team2_idx].append(home_batting.get('stolenBases'))
            self.leftOnBase[team2_idx].append(home_batting.get('leftOnBase'))
            self.earnedRuns[team2_idx].append(home_pitching.get('earnedRuns'))

            self.ops[team2_idx].append(home_batting.get('ops'))  # ops statistics
            self.era[team2_idx].append(home_pitching.get('era'))  # era statistics

    def convert_ops_era_to_df(self):
        WashOps= self.ops[0]
        NatsOps = self.ops[1]
        Washera= self.era[0]
        Natsera = self.era[1]
        Win_loss = self.record
        d = {'Wops(A)': WashOps, 'Pops(A)' :NatsOps, 'Wera(D)' : Washera, 'Pera(D)' : Natsera, 'winsW': Win_loss}
        pdf = pd.DataFrame(data=d)
        print(pdf.head(50))
        return pdf


# Returns a GamesBetweenTeamsClass given these arguments
def getGamesBetweenTeams(team1_id, team2_id, start_date='input start mm/dd/YY', end_date='input end mm/dd/YY'):
    return GamesBetweenTeams(team1_id=team1_id, team2_id=team2_id, start_date=start_date, end_date=end_date)


def getTeamIdFromTeamName(team_name):
    # If the key already exists, use that
    if team_name in team_id_dict:
        return team_id_dict.get(team_name)

    # Otherwise, create a key.
    team_id = 'Add HTML call here and a getter'
    team_id_dict.add({team_name: team_id})

    return team_id


# def convert_ops_era_to_df():
#     WashOps= test.ops[0]
#     NatsOps = test.ops[1]
#     Washera= test.era[0]
#     Natsera = test.era[1]
#     d = {'Wops': WashOps, 'Nops' :NatsOps, 'Wera' : Washera, 'Nera' : Natsera}
#     pdf = pd.DataFrame(data=d)
#     return pdf
#     print(pdf.head(50))


# test case for to run in cmd or terminal
# win percentage can be found online by looking up win the schedule of the team and the year
# i.e. Nationals schedule 2019 almanac. I like the baseball almanac site
# https://www.baseball-almanac.com/teamstats/schedule.php?y=2019&t=WS0
# if no end date is given, then the current date will be used as the end date


# hit = GamesBetweenTeamsClass(143, 120, '01/01/2019', '12/31/2019')
# test = GamesBetweenTeams(143, 120, '01/01/2015', '12/31/2019')
# nats = GamesBetweenTeamsClass(120, 143, '01/01/2019', '12/31/2019')
# print(test.games)
# test.setStats()
#
# test.getAllGames()
# phillies.getAllGames()
# nats.getAllGames()
# print(test.games)

# print(test.start_date)
# print("\n")
# print(test.end_date)
# print("\n")
# print(test.runs)
# print("\n")
# print(test.doubles)

# print("\n")
# print(test.triples)
# print("\n")
# print(test.homeRuns)
# print("\n")
# print(test.strikeOuts)
# print("\n")
# print(test.baseOnBalls)
# print("\n")
# print(test.hits)
# print("\n")
# print(test.avg)
# print("\n")
# print(test.atBats)
# print("\n")
# print(test.obp)
# print("\n")
# print(test.slg)
# print("\n")
# print(test.stolenBases)
# print("\n")
# print(test.leftOnBase)
# print("\n")
# print(test.earnedRuns)
# print("\n")
# test.convert_ops_era_to_df()

# print(phillies.ops)
# print("\n")
# print(nats.ops)
# print("\n")
# print(phillies.era)
# print("\n")
# print(nats.era)
# print("\n")


# print(test.getWinRate())
# test = GamesBetweenTeamsClass(120, 121, '01/01/2019', '')
# print(test.getWinRate())
