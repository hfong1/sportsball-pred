import statsapi
from datetime import date

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
    games = None

    win_rate = -1

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

        if (end_date == '' or end_date == None):
            end_date = date.today().strftime('%m/%d/%Y')
        self.games = statsapi.schedule(start_date=start_date,end_date=end_date,team=team1_id,opponent=team2_id)
        self.getGamesSeason()   #only look at regular season games (non including preseason or playoff games)

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

        if(len(self.games) == 0):
            return(f"No games were played between the {self.team1} and the {self.team2}")
        # Traverse through games.
        for game in self.games:
            if(game.get('winning_team')==self.team1):
                team1_wins+=1
            elif(game.get('winning_team')==self.team2):
                team1_losses+=1
            elif(game.get('status')=='Final: Tied'):
                team1_ties+=1

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

    # right now this funciton will change the self.games to only be the games from the regular season
    def getGamesSeason(self):       
        season_games = []
        for game in self.games:
            if (game.get('game_type') == 'R'):      #if the game is a regular season game
                season_games.append(game)

        self.games = season_games
        return
    
    # similar to getTeamIdFromTeamName except it gets the name from the id
    def lookUpTeamName(self, team_id):
        for key, value in team_id_dict.items():
            if team_id == value:
                return key
        return "DNE"        #does not exist


# Returns a GamesBetweenTeamsClass given these arguments
def getGamesBetweenTeams(team1_id, team2_id, start_date='input start mm/dd/YY', end_date=None):
    return GamesBetweenTeams(team1_id=team1_id, team2_id=team2_id, start_date=start_date, end_date=end_date)


def getTeamIdFromTeamName(team_name):
    # If the key already exists, use that
    if team_name in team_id_dict:
        return team_id_dict.get(team_name)

    # Otherwise, create a key.
    team_id = 'Add HTML call here and a getter'
    team_id_dict.add({team_name: team_id})

    return team_id


# And the remaining structure would look something like this... for now.
# def getDoubles(game_dict):
#     pass


# test case for to run in cmd or terminal
# win percentage can be found online by looking up win the schedule of the team and the year
# i.e. Nationals schedule 2019 almanac. I like the baseball almanac site
# https://www.baseball-almanac.com/teamstats/schedule.php?y=2019&t=WS0
# if no end date is given, then the current date will be used as the end date
# test = GamesBetweenTeams(120, 121, '01/01/2020', '12/31/2020')
# print(test.getWinRate())
# test = GamesBetweenTeams(120, 121, '01/01/2019', '')
# print(test.getWinRate())
