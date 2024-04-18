from django.urls import path

from . import views

urlpatterns = [
    path('', views.board_overview_page, name="board"),
    path('<str:club_url>/<int:constitution_pk>/review', views.review_constitution_page, name="review_constitution"),
]