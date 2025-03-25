from app.models import  *
from django.db import models
class Product(models.Model):
    title = models.CharField( max_length=50,null=True,blank=True )
    content =models.TextField(null=True,blank=True)
    price = models.DecimalField( max_digits=12, decimal_places=2,default=99.99)

    @property
    def sale_price(self):
        return "%.2f" %(float(self.price)*0.8)
    
    def get_discounts(self):
       
        return '122'
