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
    purpose=models.CharField(max_length=200,default='pay',null=True,blank=True)
    trc20_address=models.CharField(max_length=300,null=True,blank=True,default=None)
    bep20_address=models.CharField(max_length=300,null=True,blank=True,default=None)
    method=models.CharField(max_length=200,null=True,blank=True)
    state=models.BooleanField(default=False)
    time=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer.name + ' '+self.coin.name

