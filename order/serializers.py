from rest_framework import serializers
from rest_framework import response
from accounts.models import *
from payment.models import *
from .models import *
from currency.models import *




class OrderSerializer(serializers.ModelSerializer):
    customer= serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    coin = serializers.PrimaryKeyRelatedField(queryset=Method.objects.all())
    


    class Meta:
        model = Order
        fields = ['customer','account_details', 'coin', 'amount','order_email', 'method','state']

    def create(self, validated_data):
        customer = validated_data.pop('customer')
        coin = validated_data.pop('payment')
        mymodel_instance = Order.objects.create(**validated_data)
        mymodel_instance.customer= customer
        mymodel_instance.method = coin
        mymodel_instance.save()
        return mymodel_instance