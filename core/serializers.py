from rest_framework import serializers
from core.models import Post, User, Category, Comment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    category = CategorySerializer()

    class Meta:
        model = Post
        fields = ['id', 'title', 'excerpt', 'body', 'slug', 'published_at', 'user', 'category']

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    replies = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_at', 'user', 'parent', 'replies', 'likes_count']

    def get_replies(self, obj):
        replies = obj.replies.all().select_related('user').order_by('created_at')
        return CommentSerializer(replies, many=True).data

    def get_likes_count(self, obj):
        return obj.likes.count()
