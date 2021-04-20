from django.urls import reverse_lazy
from django.shortcuts import render
from baseballPred.GamesBetweenTeams import getGamesBetweenTeams
from django.http import JsonResponse
from django.views.generic import TemplateView, FormView
from baseballPred.forms import TeamSelectForm
from baseballPred.BNET import Bnet


class IndexView(TemplateView):
    template_name = 'index.html'


class DataView(TemplateView):
    template_name = 'data.html'
    team_id_dict = {
        # National League
        'Arizona Diamondbacks': 109,
        'Chicago Cubs': 112,
        'Cincinnati Reds': 113,
        'Colorado Rockies': 115,
        'Los Angeles Dodgers': 119,
        'Washington Nationals': 120,
        'New York Mets': 121,
        'Pittsburgh Pirates': 134,
        'San Diego Padres': 135,
        'San Francisco Giants': 137,
        'St. Louis Cardinals': 138,
        'Philadelphia Phillies': 143,
        'Atlanta Braves': 144,
        'Miami Marlins': 146,
        'Milwaukee Brewers': 158,
        # American League
        'Los Angeles Angels': 108,
        'Baltimore Orioles': 110,
        'Boston Red Sox': 111,
        'Cleveland Indians': 114,
        'Detroit Tigers': 116,
        'Houston Astros': 117,
        'Kansas City Royals': 118,
        'Oakland Athletics': 133,
        'Seattle Mariners': 136,
        'Tampa Bay Rays': 139,
        'Texas Rangers': 140,
        'Toronto Blue Jays': 141,
        'Minnesota Twins': 142,
        'Chicago White Sox': 145,
        'New York Yankees': 147
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['team_id_dict'] = self.team_id_dict
        return context

    @staticmethod
    def ajax_get_team_winrates(request):
        team1_id = int(request.GET.get('team1'))
        team2_id = int(request.GET.get('team2'))
        games = getGamesBetweenTeams(team1_id, team2_id, '01/01/2015', '12/31/2020')

        winrate = games.getWinRate()
        found = True
        try:
            winrate = round(float(winrate), 5)
        except ValueError:
            found = False

        data = {
            'found': found,
            'team1_winrate': winrate,
            'team1_name': games.team1,
            'team2_name': games.team2,
        }
        return JsonResponse(data)

    @staticmethod
    def ajax_get_bn_wr(request):
        team1_id = int(request.GET.get('team1'))
        team2_id = int(request.GET.get('team2'))
        games = getGamesBetweenTeams(team1_id, team2_id, '01/01/2015', '12/31/2020')
        bnet = Bnet(games)
        var_ranges = bnet.get_ranges()
        bnWR = round(bnet.get_bnet_wr(games, 5, 5), 5)

        data = {
            'team1_bnwinrate': bnWR,
            'team1_name': games.team1,
            'team2_name': games.team2,
            'wops_range': var_ranges['wops'],
            'pops_range': var_ranges['pops'],
            'wera_range': var_ranges['wera'],
        }
        return JsonResponse(data)


class TableTeamSelectView(FormView):
    template_name = 'forms/pick_team.html'
    form_class = TeamSelectForm
    success_url = reverse_lazy('baseballPred:stats_table')


class TableView(TemplateView):
    template_name = 'table.html'

    @staticmethod
    def flip_team_data(data):
        new_dict = {}
        for idx in range(len(data['dates'])):
            id = data['dates'][idx]
            new_dict[id] = {
                'runs': data['runs'][idx],
                'doubles': data['doubles'][idx],
                'triples': data['triples'][idx],
                'homeRuns': data['homeRuns'][idx],
                'strikeOuts': data['strikeOuts'][idx],
                'baseOnBalls': data['baseOnBalls'][idx],
                'hits': data['hits'][idx],
                'avg': data['avg'][idx],
                'atBats': data['atBats'][idx],
                'obp': data['obp'][idx],
                'slg': data['slg'][idx],
                'record': data['record'][idx],
                'ops': data['ops'][idx],
                'stolenBases': data['stolenBases'][idx],
                'leftOnBase': data['leftOnBase'][idx],
                'era': data['era'][idx],
                'earnedRuns': data['earnedRuns'][idx],
            }
        return new_dict

    def get_context_data(self, team1_id, team2_id, **kwargs):
        context = super().get_context_data(**kwargs)

        print("retrieve records")
        games = getGamesBetweenTeams(team1_id, team2_id, '01/01/2019', '12/31/2020')
        print("load variables")
        games.setStats()

        context['table_tags'] = [
            'dates',
            'runs',
            'doubles',
            'triples',
            'homeRuns',
            'strikeOuts',
            'baseOnBalls',
            'hits',
            'avg',
            'atBats',
            'obp',
            'slg',
            'record',
            'ops',
            'stolenBases',
            'leftOnBase',
            'era',
            'earnedRuns',
        ]

        context['team1_name'] = games.team1
        context['team2_name'] = games.team2
        context['team1'], context['team2'] = games.getStats()
        context['team1'] = self.flip_team_data(context['team1'])
        context['team2'] = self.flip_team_data(context['team2'])
        context['team1avg'], context['team2avg'] = games.getStatAverages()
        return context

    def get(self, request, *args, **kwargs):
        team1_id = int(request.GET.get('team1_id'))
        team2_id = int(request.GET.get('team2_id'))
        context = self.get_context_data(team1_id, team2_id)

        return render(request, self.template_name, context)
