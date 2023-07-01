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

    def validate(self,attrs):
        customer=User.objects.get(name=attrs.get('customer'))
        ad=attrs.get('account_details')
        co=Method.objects.get(id=attrs.get('coin'))
        am=float(attrs.get('amount'))
        oe=attrs.get('order_email')
        me=attrs.get('method')
        st=attrs.get('state')
        order=Order.objects.create(customer=customer,account_details=ad,coin=co,amount=am,order_email=oe,method=me,state=st)
        return order