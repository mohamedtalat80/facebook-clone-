from django.db import models
from django.contrib.auth.models import User 
def profile_image_upload_path(instance, filename):
    # 'instance' is the Profile instance, and 'filename' is the original file name
    return f'profile_pictures/{instance.user.username}/{filename}'
# Create your models here.
class post(models.Model):
    user=models.ForeignKey(User, verbose_name="username", on_delete=models.CASCADE)
    title=models.CharField( max_length=50)
    content=models.TextField()
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True,auto_now_add=False)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    def __str__(self):
        return self.title+"\n "+self.content    
class like(models.Model):
    user_like=models.ForeignKey(User,on_delete=models.CASCADE)
    post_like=models.ForeignKey(post,on_delete=models.CASCADE,related_name='likes')
    liked=models.BooleanField(default=False)
class comment (models.Model):
    user_comment=models.ForeignKey(User,on_delete=models.CASCADE)
    post_comment=models.ForeignKey(post,on_delete=models.CASCADE,related_name='comments')
    comment_content=models.TextField(max_length=400,null=True,blank=True)
    likes_of_comment=models.ForeignKey(like,on_delete=models.CASCADE,null=True,blank=True)
    created_at=models.DateTimeField(auto_now=False, auto_now_add=True)
    updated=models.BooleanField(default=False,null=True,blank=True)
    image = models.ImageField(upload_to='post_images/comments_images', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False,null=True,blank=True)
    reply=models.ForeignKey('self',on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    is_reply=models.BooleanField(default=False,null=True)
    def __str__(self):
        if self.is_reply:
            return f"Reply by {self.user_comment.username} to {self.reply.user_comment.username}'s comment"
        return f"Comment by {self.user_comment.username} on {self.post_comment.title}"

        

class profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to=profile_image_upload_path, null=True, default='defaultpic.jpg')
    bio = models.TextField(max_length=300, null=True,blank=True)
    date_of_birth = models.DateField(null=True,blank=True)
    status = models.CharField(max_length=150, null=True,blank=True)
    lives_in = models.CharField(max_length=150, null=True,blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

