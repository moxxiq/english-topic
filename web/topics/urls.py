from django.urls import path

from . import views

app_name = 'topics'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:topic_id>/', views.topic, name='topic')
]
