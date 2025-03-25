from rest_framework import serializers
from .models import Product
from .models import post
from .models import like        
from .models import comment
from .models import profile
from django.contrib.auth.models import User
class productserializer(serializers.ModelSerializer):
    discounts=serializers.SerializerMethodField()
    class Meta:
        model=Product
        fields=['title','content','price','sale_price','discounts']
    
    def get_discounts(self,obj):
        if not hasattr(obj,'id'):
            return None
        if isinstance(obj,Product):
            return None

        return obj.get_discounts()
class Post_Detailed_Serializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())  # عرض اسم المستخدم بدل ID

    class Meta:
        model = post
        fields = ['id', 'user', 'title', 'content', 'created_at', 'updated_at', 'image']
        read_only_fields = ['id', 'created_at', 'updated_at']  # منع التعديل على هذه الحقول
class Post_Serializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)  # عرض اسم المستخدم بدل ID

    class Meta:
        model = post
        fields = ['id', 'user', 'title', 'content',"image"]
        read_only_fields = ['id']  # منع التعديل على هذه الحقول
        
class LikeSerializer(serializers.ModelSerializer):
    user_like = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())  # يرجع ID المستخدم فقط
    post_like = serializers.PrimaryKeyRelatedField(queryset=post.objects.all())  # يرجع ID البوست فقط

    class Meta:
        model = like
        fields = ['id', 'user_like', 'post_like', 'liked']
        read_only_fields = ['id', 'user_like', 'post_like']  # منع التعديل على هذه الحقول
class Comment_Detailed_Serializer(serializers.ModelSerializer):
    user_comment = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    post_comment = serializers.PrimaryKeyRelatedField(queryset=post.objects.all())  # ID البوست فقط
    replies = serializers.SerializerMethodField()  # لعرض الردود

    def get_replies(self, obj):
        # جلب الردود بشكل متداخل مع حد أقصى للتجنب اللانهائي
        if obj.replies.exists():
            return Comment_Detailed_Serializer(obj.replies.all(), many=True).data
        return []

    class Meta:
        model = comment
        fields = ['id', 'user_comment', 'post_comment', 'comment_content', 'created_at', 
                  'updated', 'updated_at', 'image', 'is_reply', 'replies']
        read_only_fields = ['id', 'created_at', 'updated_at']       
class Comment_Serializer(serializers.ModelSerializer):
    user_comment = serializers.CharField(source='user_comment.username', read_only=True)
    post_comment = serializers.PrimaryKeyRelatedField(read_only=True)  # ID البوست فقط
    class Meta:
        model=comment
        fields=['id','user_comment','post_comment','comment_content','image','created_at','is_reply']    
        read_only_fields=['id','user_comment','post_comment','created_at','updated_at']

class Profile_Detailed_Serializer(serializers.ModelSerializer):   
    class Meta:
        model=profile
        fields=['user','profile_pic','bio','date_of_birth','status','lives_in']
class Profile_Serializer(serializers.ModelSerializer):   
    class Meta:
        model=profile
        fields=['id','user','profile_pic',]
    