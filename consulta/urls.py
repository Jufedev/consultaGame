from django.urls import path
from . import views

urlpatterns = [
    path("", views.search),
    path("game/", views.game)
]
