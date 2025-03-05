from rest_framework import serializers
from .models import Product

class productserializer(serializers.ModelSerializer):
    discounts=serializers.SerializerMethodField()
    class Meta:
        model=Product
        fields=['title','content','price','sale_price','discounts']
    
    def get_discounts(self,obj):
        if not hasattr(obj,'id'):
            return None
        if isinstance(obj,Product):
            return None

        return obj.get_discounts()
        
    