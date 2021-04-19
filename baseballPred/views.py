from django.urls import reverse_lazy
from baseballPred.GamesBetweenTeams import getGamesBetweenTeams
from django.http import JsonResponse
from django.views.generic import TemplateView, FormView


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
        games = getGamesBetweenTeams(team1_id, team2_id, '01/01/2019', '12/31/2020')

        winrate = games.getWinRate()
        found = True
        try:
            winrate = float(winrate)
        except ValueError:
            found = False

        games.setStats()
        team1, team2 = games.getStats()
        team1avg, team2avg = games.getStatAverages()

        data = {
            'found': found,
            'team1_winrate': winrate,
            'team1_name': games.team1,
            'team2_name': games.team2,
            'team1': team1,
            'team2': team2,
            'team1avg': team1avg,
            'team2avg': team2avg,
        }
        return JsonResponse(data)


# class TableTeamSelectView(FormView):
#     template_name = ''
#     form_class = TeamSelectForm
#     success_url = reverse_lazy('')

#
# class TableView(TemplateView):
#     template_name = 'table.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['team1'], context['team2'] =
#
#     @staticmethod
#     def ajax_get_team_data(request):
#         team1_id = int(request.GET.get('team1'))
#         team2_id = int(request.GET.get('team2'))
#         games = getGamesBetweenTeams(team1_id, team2_id, '01/01/2020', '12/31/2020')
#         games.setStats()
#         team1, team2 = games.getStats()
#         data = {
#             'team1': team1,
#             'team2': team2,
#         }
#         return JsonResponse(data)
