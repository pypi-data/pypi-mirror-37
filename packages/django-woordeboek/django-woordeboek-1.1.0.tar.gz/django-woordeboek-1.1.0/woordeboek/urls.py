from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('api/', views.APIView.as_view(), name='api'),
    path('stats/', views.StatsView.as_view(), name='stats'),
]

app_name = 'woordeboek'