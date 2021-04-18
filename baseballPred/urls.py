from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'baseballPred'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('data/', views.DataView.as_view(), name='data'),
    path('ajax/data/teams/', views.DataView.ajax_get_team_winrates, name='ajax_get_team_winrates')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
