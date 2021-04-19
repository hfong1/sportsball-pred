from django.forms import Form, CharField, TypedChoiceField


TEAM_CHOICES = [
    # National League
    (109, 'Arizona Diamondbacks'),
    (112, 'Chicago Cubs'),
    (113, 'Cincinnati Reds'),
    (115, 'Colorado Rockies'),
    (119, 'Los Angeles Dodgers'),
    (120, 'Washington Nationals'),
    (121, 'New York Mets'),
    (134, 'Pittsburgh Pirates'),
    (135, 'San Diego Padres'),
    (137, 'San Francisco Giants'),
    (138, 'St. Louis Cardinals'),
    (143, 'Philadelphia Phillies'),
    (144, 'Atlanta Braves'),
    (146, 'Miami Marlins'),
    (158, 'Milwaukee Brewers'),
    # American League
    (108, 'Los Angeles Angels'),
    (110, 'Baltimore Orioles'),
    (111, 'Boston Red Sox'),
    (114, 'Cleveland Indians'),
    (116, 'Detroit Tigers'),
    (117, 'Houston Astros'),
    (118, 'Kansas City Royals'),
    (133, 'Oakland Athletics'),
    (136, 'Seattle Mariners'),
    (139, 'Tampa Bay Rays'),
    (140, 'Texas Rangers'),
    (141, 'Toronto Blue Jays'),
    (142, 'Minnesota Twins'),
    (145, 'Chicago White Sox'),
    (147, 'New York Yankees'),
]


class TeamSelectForm(Form):
    team1_id = TypedChoiceField(label="Team 1", choices=TEAM_CHOICES, coerce=int)
    team2_id = TypedChoiceField(label="Team 2", choices=TEAM_CHOICES, coerce=int)
