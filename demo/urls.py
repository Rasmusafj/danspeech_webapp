from . import views

from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('preprocess_audio/', views.preprocess_webm, name='preprocess_audio'),
    path('transcribe/', views.transcribe, name='transcribe'),
    path('update_config/', views.update_config, name='update_config'),
]
