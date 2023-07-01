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

    def validate(self, attrs):
        #cu=User.objects.get(id=attrs.get('customer'))
        ad=attrs.get('account_details')
        #co=Method.objects.get(id=attrs.get('coin'))
        print(attrs.get('customer'))
        am=attrs.get('amount')
        oe=attrs.get('order_email')
        me=attrs.get('method')
        st=attrs.get('state')
        order=Order.objects.create(
            customer=attrs.get('customer'),
            account_details=ad,
            coin=attrs.get('coin'),
            amount=am,
            order_email=oe,
            method=me,
            state=st
        )
        return order

        