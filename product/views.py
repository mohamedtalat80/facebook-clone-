from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
from django.shortcuts import render,get_object_or_404
from .models import Product
from api.serializers import productserializer

class ProductDetailview(generics.RetrieveAPIView):
    queryset=Product.objects.all()
    serializer_class=productserializer

product_detailview=ProductDetailview.as_view() #for clean code perpouses only
class ProductcCreateview(generics.CreateAPIView):
    queryset=Product.objects.all()
    serializer_class=productserializer

Productccreateview=ProductcCreateview.as_view() #for clean code perpouses only

class ProductcUpdateview(generics.UpdateAPIView):
    queryset=Product.objects.all()
    serializer_class=productserializer

ProductUpdateview=ProductcUpdateview.as_view() #for clean code perpouses only
class ProductcCreateview(generics.CreateAPIView):
    queryset=Product.objects.all()
    serializer_class=productserializer
    lookup_field='pk'
    def preform_creation(self,request):
        serializer=productserializer(request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        
        
        
Productccreateview=ProductcCreateview.as_view() #for clean code perpouses only

@api_view(["GET","post"])
def APIVIEW(request,pk=None,*args, **kwargs):
    if request.method=='GET':
        if pk is not None:
            obj= get_object_or_404(Product,pk=pk) 
            data=productserializer(obj,many=False)
            return Response(data.data)
        alldata=Product.objects.all()
        serializer=productserializer(alldata)
        return Response(serializer.data)
    if request.method=='POST':
        serializer=productserializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data)