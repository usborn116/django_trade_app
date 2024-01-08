from django.urls import path

from . import views

app_name = "trade_app"

urlpatterns = [
    path('', views.index, name="index"),
    path("league/<int:pk>", views.LeagueView.as_view(), name="league"),
    path("teams/<int:pk>", views.RosterView.as_view(), name="roster"),
    path("player/<int:pk>", views.PlayerView.as_view(), name="player"),
    path("trade_form/<int:pk>/", views.trade_form, name="trade_form"),
    path("player_trade_form/<int:t1>/<int:t2>/", views.player_trade_form, name="player_trade_form"),
    path("trade_results/<str:give>/<str:get>", views.trade_results, name="trade_results"),
]