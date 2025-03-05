from django.urls import path
from .views import *
urlpatterns = [
    # path('<int:pk>/',product_detailview),
    path('<int:pk>/',APIVIEW)
]
