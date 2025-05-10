# favorites/views.py
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Favorite

class FavoritesListView(LoginRequiredMixin, ListView):
    model = Favorite
    template_name = "favorites/favorites_list.html"
    context_object_name = "favorites"
