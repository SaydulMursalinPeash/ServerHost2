from rest_framework import serializers
from rest_framework import response
from accounts.models import *
from payment.models import *
from .models import *
from currency.models import *




class OrderSerializer(serializers.ModelSerializer):
    
    


    class Meta:
        model = Order
        fields = ['customer','account_details', 'coin', 'amount','order_email', 'method','state']

    def create(self, validated_data):
        customer1 = validated_data.pop('customer')
        customer=User.objects.get(id=customer1)
        c = validated_data.pop('coin')
        coin=Method.objects.get(id=c)
        
        mymodel_instance = Order.objects.create(**validated_data)
        mymodel_instance.customer= customer
        mymodel_instance.method = coin
        mymodel_instance.save()
        return mymodel_instance