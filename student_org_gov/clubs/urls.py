from django.urls import path
from .views import clubs_page, club_page, constitution_page, edit_constitution_page, create_club_page, delete_constitution, delete_club, submit_constitution, review_constitution, save_constitution_edits, remove_article_constitution, add_article_constitution, remove_section_constitution, add_section_constitution

urlpatterns = [
    path("", clubs_page.view, name="clubs"),
    path('<str:club_url>/', club_page.view, name="club"),
    path('<str:club_url>/<int:constitution_pk>/', constitution_page.view, name="constitution"),
    path('<str:club_url>/edit_constitution', edit_constitution_page.view, name="edit_constitution"),
    path('createclub', create_club_page.view, name="create_club"),

    path('delete_constitution.x', delete_constitution.view, name="delete_constitution"),
    path('delete_club.x', delete_club.view, name="delete_club"),
    path('<str:club_url>/submit_constitution.x', submit_constitution.view, name="submit_constitution"),
    path('review_constitution.x', review_constitution.view, name="review_constitution"),
    path('<str:club_url>/save_constitution_edits.x', save_constitution_edits.view, name="save_constitution_edits"),
    path('remove_article_constitution.x', remove_article_constitution.view, name="remove_article_constitution"),
    path('add_article_constitution.x', add_article_constitution.view, name="add_article_constitution"),
    path('remove_section_constitution.x', remove_section_constitution.view, name="remove_section_constitution"),
    path('add_section_constitution.x', add_section_constitution.view, name="add_section_constitution"),
]