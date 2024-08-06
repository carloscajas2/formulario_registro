from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('manage/', views.manage_view, name='manage'),
    path('download_excel/', views.download_excel, name='download_excel'),
]
