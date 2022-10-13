from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search_link'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('autos/', views.AutoListView.as_view(), name="autos_link"),
    path('manouzsakymai/', views.UzsakymasListView.as_view(), name='mano_uzsakymai'),
    path('manouzsakymai/<int:pk>', views.UzsakymasDetailView.as_view(), name='uzsakymas_detail'),
    path('profilis/', views.profilis, name='profilis'),
    path('register/', views.register, name='register'),


]