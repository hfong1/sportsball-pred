from django.urls import path
from . import views

app_name = 'baseballPred'
urlpatterns = [
    path('', views.index, name='index'),
    path('data/', views.data, name='data'),
    path('ajax/data/teams/', views.ajax_get_team_winrates, name='ajax_get_team_winrates')
]
