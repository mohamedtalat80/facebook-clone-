from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import post, comment, like
from django.core.files.uploadedfile import SimpleUploadedFile
class PostAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client.login(username="testuser", password="testpassword")

        
        # Create a sample post
        self.post = post.objects.create(
            user=self.user, 
            title="Test Post", 
            content="This is a test post", 
            image=None
        )
    
    def test_get_posts(self):
        # Test fetching all posts
        response = self.client.get('/api/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)  # At least one post should exist

    def test_create_post(self):
        # Test creating a new post
        image_file = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
        data = {
            "title": "New Post",
            "content": "This is a new post",
            # "image" : image_file
        }
        response = self.client.post('/api/posts/', data)
        
        title = response.data.get("title")
        self.assertEqual(title, "New Post", f"Expected 'New Post', but got {title}")
        # self.assertEqual(response.data["title"], "New Post")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_post(self):
        # Test updating an existing post
        image_file = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
        data = {
            "title": "Updated Post",
            "content": "This is an updated post",
            # "image" : image_file
        }
        response = self.client.put(f'/api/posts/{self.post.id}/', data)
        self.assertEqual(response.data["title"], "Updated Post")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_post(self):
        # Test deleting a post
        response = self.client.delete(f'/api/posts/{self.post.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(post.objects.filter(id=self.post.id).exists())
class LikeAPITestCase(APITestCase):
    def setUp(self):
        # إنشاء مستخدم وتسجيل الدخول
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client.login(username="testuser", password="testpassword")
        
        # إنشاء منشور
        self.post = post.objects.create(user=self.user, title="Test Post", content="This is a test post")
    
    def test_toggle_like(self):
        # بيانات اللايك
        data = {"post_id": self.post.id}
        
        # إضافة لايك
        response = self.client.post('/api/likes/toggle_like/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(like.objects.filter(post_like=self.post, user_like=self.user).exists())
        
        # إزالة اللايك
        response = self.client.post('/api/likes/toggle_like/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(like.objects.filter(post_like=self.post, user_like=self.user).exists())

class CommentAPITestCase(APITestCase):
    def setUp(self):
        # إنشاء مستخدم وتسجيل الدخول
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client.login(username="testuser", password="testpassword")
        
        # إنشاء منشور
        self.post = post.objects.create(user=self.user, title="Test Post", content="This is a test post")
    
    def test_add_comment(self):
        # بيانات التعليق
        data = {
            "post_comment": self.post.id,  # ID المنشور اللي هنضيف عليه التعليق
            "comment_content": "This is a test comment"
        }
        
        # إرسال الطلب
        response = self.client.post('/api/comments/', data)
        print(response.data)
        # التحقق من النتيجة
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["comment_content"], "This is a test comment")
