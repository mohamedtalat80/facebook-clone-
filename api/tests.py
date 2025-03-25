from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import post, comment, like ,profile 
from django.core.files.uploadedfile import SimpleUploadedFile
class PostAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.post = post.objects.create(user=self.user, title="Test Post", content="This is a test post")

    def test_get_posts(self):
        response = self.client.get('/api/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Test Post")

    def test_get_post_light(self):
        response = self.client.get(f'/api/posts/{self.post.id}/read/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Test Post")
        

    def test_create_post(self):
        data = {"title": "New Post", "content": "This is a new post", "user": self.user.id}
        response = self.client.post('/api/posts/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "New Post")

    def test_update_post(self):
        data = {"user":self.user.id,"title": "Updated Post", "content": "This is an updated post"}
        response = self.client.put(f'/api/posts/{self.post.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Updated Post")

    def test_delete_post(self):
        response = self.client.delete(f'/api/posts/{self.post.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(post.objects.filter(id=self.post.id).exists())

class LikeAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.post = post.objects.create(user=self.user, title="Test Post", content="This is a test post")

    def test_get_likes(self):
        like.objects.create(user_like=self.user, post_like=self.post, liked=True)
        response = self.client.get('/api/likes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_like(self):
        data = {"user_like": self.user.id, "post_like": self.post.id, "liked": True}
        response = self.client.post('/api/likes/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(like.objects.filter(post_like=self.post, user_like=self.user).exists())

    def test_delete_like(self):
        like_obj = like.objects.create(user_like=self.user, post_like=self.post, liked=True)
        response = self.client.delete(f'/api/likes/{like_obj.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(like.objects.filter(id=like_obj.id).exists())

class CommentAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.post = post.objects.create(user=self.user, title="Test Post", content="This is a test post")

    def test_get_comments(self):
        comment.objects.create(user_comment=self.user, post_comment=self.post, comment_content="Test Comment")
        response = self.client.get('/api/comments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_comment_light(self):
        comment_obj = comment.objects.create(user_comment=self.user, post_comment=self.post, comment_content="Test Comment")
        response = self.client.get(f'/api/comments/{comment_obj.id}/read/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["comment_content"], "Test Comment")
        self.assertNotIn("replies", response.data)  # النسخة الخفيفة ما فيهاش replies

    def test_add_comment(self):
        data = {"post_comment": self.post.id, "comment_content": "This is a test comment", "user_comment": self.user.id}
        response = self.client.post('/api/comments/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["comment_content"], "This is a test comment")

    def test_update_comment(self):
        comment_obj = comment.objects.create(user_comment=self.user, post_comment=self.post, comment_content="Test Comment")
        
        data = {"user_comment":self.user.id,"post_comment":self.post.id, "comment_content": "This is an updated comment"}
        response = self.client.put(f'/api/comments/{comment_obj.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["comment_content"], "This is an updated comment")

    def test_delete_comment(self):
        comment_obj = comment.objects.create(user_comment=self.user, post_comment=self.post, comment_content="Test Comment")
        response = self.client.delete(f'/api/comments/{comment_obj.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(comment.objects.filter(id=comment_obj.id).exists())

    def test_add_reply(self):
        parent_comment = comment.objects.create(user_comment=self.user, post_comment=self.post, comment_content="Test Comment")
        data = {"post_comment": self.post.id, "comment_content": "This is a test reply", "reply": parent_comment.id, "user_comment": self.user.id}
        response = self.client.post('/api/comments/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["comment_content"], "This is a test reply")

    def test_update_reply(self):
        parent_comment = comment.objects.create(user_comment=self.user, post_comment=self.post, comment_content="Test Comment")
        reply = comment.objects.create(user_comment=self.user, post_comment=self.post, comment_content="Test Reply", reply=parent_comment)
        data = {"user_comment":self.user.id,"post_comment":self.post.id,"comment_content": "Updated Reply"}
        response = self.client.put(f'/api/comments/{reply.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["comment_content"], "Updated Reply")

    def test_delete_reply(self):
        parent_comment = comment.objects.create(user_comment=self.user, post_comment=self.post, comment_content="Test Comment")
        reply = comment.objects.create(user_comment=self.user, post_comment=self.post, comment_content="Test Reply", reply=parent_comment)
        response = self.client.delete(f'/api/comments/{reply.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(comment.objects.filter(id=reply.id).exists())

class ProfileAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="helloworld", password="testpassword")
        self.user_for_creation=User.objects.create_user(username="ahmed", password="testpassword")
        self.profile=profile.objects.create(user=self.user, bio="Test Bio", date_of_birth="2000-01-01", status="Single", lives_in="Cairo")

    def test_get_profiles(self):
        response = self.client.get('/api/profiles/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["bio"], "Test Bio")

    def test_get_profile_light(self):
        response = self.client.get(f'/api/profiles/{self.profile.id}/read/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
      

    def test_create_profile(self):
        
        data = {
    "user": self.user_for_creation.id,
    "bio": "New Bio",
    "date_of_birth": "2000-01-01",
    "status": "Single",
    "lives_in": "Cairo"
    }
        response = self.client.post('/api/profiles/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["bio"], "New Bio")

    def test_update_profile(self):
        data = {"user":self.user.id,"bio": "Updated Bio"}
        response = self.client.put(f'/api/profiles/{self.profile.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["bio"], "Updated Bio")

    def test_delete_profile(self):
        response = self.client.delete(f'/api/profiles/{self.profile.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(profile.objects.filter(id=self.profile.id).exists())
