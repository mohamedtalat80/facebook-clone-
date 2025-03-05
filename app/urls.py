from django.urls import path,include

from django.conf import settings
from django.conf.urls.static import static
from .views import *
from rest_framework.routers import DefaultRouter
from .views import PostViewSet,CommentViewSet,LikeViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'likes', LikeViewSet)
urlpatterns=[
 
    # path('', form_view, name='formss'),
    path('',home,name='home'),
    path('home',home,name='home'),
    path('createpost',createpost,name='createpost'),
    path('register',register,name='register'),
    path('logout',log_out,name='log_out'),   
    path('editpost/<str:postid>', edit_post, name='edit-post'),
    path('create_profile', create_profile, name='create_profile'),
    path('<str:username>', user_posts, name='view'),
    path('reply_to_comment/<int:comment_id>/', reply_to_comment, name='reply_to_comment'),
    path('api/', include(router.urls)),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)