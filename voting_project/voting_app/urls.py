from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),

    path('vote/', views.vote, name='vote'),
    path('results/', views.results, name='results'),
    path('success/', views.success, name='success'),
]
