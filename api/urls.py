from django.urls import path,include
from .views import api_home


urlpatterns = [
     path('product/',api_home)
 ]
 