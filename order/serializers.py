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
        customer = validated_data.get('customer')
        print('-----------------------------------------------------')
        print(customer)
        customer=User.objects.get(id=customer)
        coin = validated_data.get('coin')
        coin=Method.objects.get(id=coin)
        
        mymodel_instance = Order.objects.create(**validated_data)
        mymodel_instance.customer= customer
        mymodel_instance.method = coin
        mymodel_instance.save()
        return mymodel_instance