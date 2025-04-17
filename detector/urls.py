from django.urls import path
from . import views

app_name = 'detector'

urlpatterns = [
    path('', views.index, name='index'),
    path('detect/', views.detect, name='detect'),
    path('results/<int:result_id>/', views.results, name='results'),
    path('trending/', views.trending_news, name='trending_news'),
]
