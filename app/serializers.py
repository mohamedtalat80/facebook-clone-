from rest_framework import serializers
from .models import post, comment, like, profile
from django.contrib.auth.models import User
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = comment
        fields = ['id', 'comment_content', 'created_at']
    def get_replies(self, obj):
        # هذا سيعرض الردود فقط إذا كانت موجودة
        replies = obj.replies.all()
        return CommentSerializer(replies, many=True).data

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = like
        fields = ['user_like', 'liked']
    
    
class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    likes = LikeSerializer(many=True, read_only=True)

    class Meta:
        model = post
        fields = ['id',  'title', 'content', 'image', 'created_at', 'updated_at', 'comments', 'likes']