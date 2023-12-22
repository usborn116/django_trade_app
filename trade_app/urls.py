from django.urls import path

from . import views

app_name = "trade_app"

urlpatterns = [
    path('', views.index, name="index"),
    path("teams/<int:team_id>/roster", views.roster, name="roster"),
    path("tradeform", views.trade_form, name="trade form"),
]