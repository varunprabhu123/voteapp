from django.urls import path
from . import views

urlpatterns = [
    path("", views.Register, name="register"),
    path("login/", views.Login_view, name="login"),
    path("logout/", views.Logout_view, name="logout"),
    path("vote/", views.Vote_view, name="vote"),
    path("results/", views.view_result, name="results"),
]