from django.urls import path
from . import views

app_name = 'gold_analytics'

urlpatterns = [
    path('', views.AnalyticsDashboardView.as_view(), name='dashboard'),
    
] 