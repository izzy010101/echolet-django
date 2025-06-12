from rest_framework import serializers
from core.models import Post
from core.models import User

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'excerpt', 'body', 'slug', 'published_at', 'user_id', 'category']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name']

