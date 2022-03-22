from django.urls import path

# from .views import CSVListView, CSVDetailView
from . import views


urlpatterns = [
    path("", views.home, name="spotify_home"),
    path("search", views.search, name="spotify_search"),
    path("results/", views.createSearchResults, name="results"),
    path("how-to-use/", views.how, name="how"),
    path("faq/", views.faq, name="faq"),
]
