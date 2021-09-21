from django.urls import path

from . import views




urlpatterns = [
    path("books/", views.books),
    path("books/<int:_id>/", views.book),
    path("login/", views.login),
]