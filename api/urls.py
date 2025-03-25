from django.urls import path,include
from .views import api_home,ProductList
from .views import *
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# إعدادات Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="My API",
        default_version='v1',
        description="API documentation for my project",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="your-email@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # Posts
    path('posts/', PostList.as_view(), name='post-list'),              # GET: قائمة، POST: إنشاء
    path('posts/<int:pk>/', PostApi.as_view(), name='post-detail'),    # GET, PUT, DELETE للبوست
    path('posts/<int:pk>/read/', Post_onlyread.as_view(), name='post-read'),  # GET فقط (خفيف)

    # Likes
    path('likes/', Likes.as_view(), name='like-list'),                 # GET: قائمة، POST: إنشاء
    path('likes/<int:id>/', Likes.as_view(), name='like-detail'),      # DELETE للايك

    # Comments
    path('comments/', CommentList.as_view(), name='comment-list'),     # GET: قائمة، POST: إنشاء
    path('comments/<int:pk>/', CommentApi.as_view(), name='comment-detail'),  # GET, PUT, DELETE
    path('comments/<int:pk>/read/', Comment_onlyread.as_view(), name='comment-read'),  # GET فقط (خفيف)

    # Profiles
    path('profiles/', Profile_list.as_view(), name='profile-list'),    # GET: قائمة، POST: إنشاء
    path('profiles/<int:pk>/', Profile_Api.as_view(), name='profile-detail'),  # GET, PUT, DELETE
    path('profiles/<int:pk>/read/', Profile_onlyread.as_view(), name='profile-read'),  # GET فقط (خفيف)
]