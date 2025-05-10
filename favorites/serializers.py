from rest_framework import serializers
from favorites.models import Favorite
from catalog.serializers import BookSerializer

class FavoriteSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    class Meta:
        model = Favorite
        fields = ("id", "book", "created_at")
        read_only_fields = ("id", "created_at")
