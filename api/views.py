from django.shortcuts import render
from django.http import JsonResponse
from .models import Product
import json
from .serializers import productserializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
@api_view(['POST','GET'])
def api_home(request,*args, **kwargs):
    
    instance=productserializer(data=request.data)
    if instance.is_valid():
        instance.save()
        print (instance.data)
    return Response(instance.data)    