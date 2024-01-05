from django.urls import path

from . import views

app_name = "trade_app"

urlpatterns = [
    path('', views.index, name="index"),
    path("league/<int:pk>", views.LeagueView.as_view(), name="league"),
    path("teams/<int:pk>", views.RosterView.as_view(), name="roster"),
    path("player/<int:pk>", views.PlayerView.as_view(), name="player"),
    path("tradeform", views.trade_form, name="trade form"),
]