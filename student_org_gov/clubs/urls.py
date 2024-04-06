from django.urls import path
from . import views

urlpatterns = [
    path("", views.clubs_page, name="clubs"),
    path('<str:club_url>/', views.club_page, name="club"),
    path('<str:club_url>/<int:constitution_pk>/', views.constitution_page, name="constitution"),
    path('<str:club_url>/edit_constitution', views.edit_constitution_page, name="edit_constitution"),
    path('createclub', views.create_club_page, name="create_club"),

    path('delete_constitution.x', views.delete_constitution, name="delete_constitution"),
    path('delete_club.x', views.delete_club, name="delete_club"),
    path('<str:club_url>/submit_constitution.x', views.submit_constitution, name="submit_constitution"),
    path('review_constitution.x', views.review_constitution, name="review_constitution"),
    path('<str:club_url>/save_constitution_edits.x', views.save_constitution_edits, name="save_constitution_edits"),
    path('remove_article_constitution.x', views.remove_article_constitution, name="remove_article_constitution"),
    path('add_article_constitution.x', views.add_article_constitution, name="add_article_constitution"),
    path('remove_section_constitution.x', views.remove_section_constitution, name="remove_section_constitution"),
    path('add_section_constitution.x', views.add_section_constitution, name="add_section_constitution"),
]