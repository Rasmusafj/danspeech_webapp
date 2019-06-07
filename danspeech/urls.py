from . import views
from django.urls import include, path
urlpatterns = [
    path('demo/', include('demo.urls')),
    path('', views.index, name='index'),
    path('requirements/', views.requirements, name="requiremnets"),
    path('save/', views.save_audio, name='save'),
]
