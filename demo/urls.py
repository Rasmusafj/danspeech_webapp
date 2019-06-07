from . import views

from django.urls import include, path

urlpatterns = [
    path('', views.index, name='index'),
    path('preprocess_audio/', views.preprocess_webm, name='preprocess_audio'),
    path('transcribe/', views.transcribe, name='transcribe'),
]
