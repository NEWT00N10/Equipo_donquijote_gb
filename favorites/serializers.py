from rest_framework import serializers
from favorites.models import Favorite

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ("id", "book", "created_at")
        read_only_fields = ("id", "created_at")
