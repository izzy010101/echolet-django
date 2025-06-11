from rest_framework import serializers
from core.models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'excerpt', 'body', 'slug', 'published_at', 'user_id']