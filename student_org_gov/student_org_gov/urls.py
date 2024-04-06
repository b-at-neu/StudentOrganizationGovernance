from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("home.urls")),
    path("users/", include("users.urls")),
    path("board/", include("board.urls")),
    path("clubs/", include("clubs.urls")),
    path('admin/', admin.site.urls),
]

