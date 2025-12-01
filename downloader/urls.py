from django.urls import path
from . import views

urlpatterns = [
    path('', views.download_Video, name='download_video'),
]