from django.urls import path
from . import views


urlpatterns = [
    path("signup", views.signup, name="signup"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("editrole", views.edit_role, name="edit_role"),
    path("editclub", views.edit_club, name="edit_club"),
    path("users", views.users_overview, name="users"),
]