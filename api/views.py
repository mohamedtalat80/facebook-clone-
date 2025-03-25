from django.shortcuts import render
from django.http import JsonResponse
from .models import Product , post, like, comment, profile
import json
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from django.shortcuts import get_object_or_404
@api_view(['POST','GET'])
def api_home(request,*args, **kwargs):
    
    instance=productserializer(data=request.data)
    if instance.is_valid():
        instance.save()
        print (instance.data)
    return Response(instance.data)
    
#for testing perpouse only !!
class ProductList(APIView):
    def get (self,request):
        products=Product.objects.all()
        serializer=productserializer(products,many=True)
        return Response(serializer.data)
    def post (self,request):
        if request.data is not None:
            data=request.data
            serializer=productserializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=201)
            return Response(serializer.errors,status=400)
        
        
    def put(self,request,id):
        if request.data is not None:

            data=request.data
            product_id=Product.objects.get(id=id)
            serializer=productserializer(product_id,data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=201)
            
    def delete(self,request,id):
        product_id=Product.objects.get(id=id)
        product_id.delete()
        return Response(status=204) 
class PostList(generics.ListCreateAPIView):
    queryset = post.objects.all()
    def get_serializer_class(self):
        if self.request.query_params.get('light', '').lower() == 'true':
            return Post_Serializer
        return Post_Detailed_Serializer

class PostApi(generics.RetrieveUpdateDestroyAPIView):
    queryset = post.objects.all()
    serializer_class = Post_Detailed_Serializer

class Post_onlyread(generics.RetrieveAPIView):
    queryset = post.objects.all()
    serializer_class = Post_Serializer

class Likes(APIView):
    def get(self, request):
        likes = like.objects.all()
        serializer = LikeSerializer(likes, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = LikeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def delete(self, request, id):
        like_obj = get_object_or_404(like, id=id)
        like_obj.delete()
        return Response(status=204)

class Comment_onlyread(generics.RetrieveAPIView):
    queryset = comment.objects.all()
    serializer_class = Comment_Serializer

class CommentList(generics.ListCreateAPIView):
    queryset = comment.objects.all()
    def get_serializer_class(self):
        if self.request.query_params.get('light', '').lower() == 'true':
            return Comment_Serializer
        return Comment_Detailed_Serializer

class CommentApi(generics.RetrieveUpdateDestroyAPIView):
    queryset = comment.objects.all()
    serializer_class = Comment_Detailed_Serializer

class Profile_list(generics.ListCreateAPIView):
    queryset = profile.objects.all()
    serializer_class = Profile_Detailed_Serializer

class Profile_Api(generics.RetrieveUpdateDestroyAPIView):
    queryset = profile.objects.all()
    serializer_class = Profile_Detailed_Serializer

class Profile_onlyread(generics.RetrieveAPIView):
    queryset = profile.objects.all()
    serializer_class = Profile_Serializer
    