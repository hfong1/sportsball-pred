from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'baseballPred'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('data/', views.DataView.as_view(), name='data'),
    path('ajax/data/teams/', views.DataView.ajax_get_team_winrates, name='ajax_get_team_winrates'),
    path('stats/', views.TableTeamSelectView.as_view(), name='table_team_selct'),
    path('stats/table', views.TableView.as_view(), name='stats_table'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
