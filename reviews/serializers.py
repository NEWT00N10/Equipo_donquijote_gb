from rest_framework import serializers
from reviews.models import Review

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    book = serializers.PrimaryKeyRelatedField(queryset=__import__("catalog").models.Book.objects.all())

    class Meta:
        model = Review
        fields = ("id", "book", "user", "rating", "comment", "created_at")
        read_only_fields = ("id", "user", "created_at")
