from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("wiki/<title>", views.entry, name="entry") # Every entry page should be prefixed with wiki/ -- even if lets say we have a title called search, we wont be confused with the top
]
