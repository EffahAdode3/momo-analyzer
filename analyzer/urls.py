from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_view, name='upload'),
    path('download/', views.download_csv, name='download_csv'),
]
