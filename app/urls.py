from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('manage/', views.manage_view, name='manage'),
    path('download_csv/', views.download_csv, name='download_csv'),
]
