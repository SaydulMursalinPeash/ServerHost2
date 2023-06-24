from django.db import models
from accounts.models import *
from payment.models import *
from currency.models import *

class Order(models.Model):
    customer=models.ForeignKey(User,null=True,on_delete=models.CASCADE,related_name='order_customer')
    account_details=models.TextField(max_length=2000,null=True,blank=True)
    coin=models.ForeignKey(Method,null=True,on_delete=models.CASCADE,related_name='order_method')
    amount=models.FloatField(null=True,blank=True)
    order_email=models.EmailField(null=True,blank=True)
    method=models.CharField(max_length=200,null=True,blank=True)
    state=models.CharField(max_length=200,null=True,)
    time=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer.name + ' '+self.method.name

