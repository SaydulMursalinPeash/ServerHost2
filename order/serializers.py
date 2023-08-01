from rest_framework import serializers
from rest_framework import response
from accounts.models import *
from payment.models import *
from .models import *
from currency.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','name']

class OrderSerializer(serializers.ModelSerializer):
    customer=UserSerializer()

    class Meta:
        model = Order
        fields = ['customer','account_details', 'coin', 'amount', 'method','state']


class BuyOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields=['customer','account_details', 'coin', 'amount','purpose','order_email', 'method']
        def validate(self, attrs):
        #cu=User.objects.get(id=attrs.get('customer'))
            ad=attrs.get('account_details')
            #co=Method.objects.get(id=attrs.get('coin'))
            print(attrs.get('customer'))
            am=attrs.get('amount')
            oe=attrs.get('order_email')
            pu=attrs.get('purpose')
            me=attrs.get('method')

            order=Order.objects.create(
                customer=attrs.get('customer'),
                account_details=ad,
                coin=attrs.get('coin'),
                amount=am,
                purpose=pu,
                order_email=oe,
                method=me,
            )
            return order   


class SellOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields=['customer','account_details', 'coin', 'amount','trc20_address','bep20_address', 'method']
        def validate(self, attrs):
        #cu=User.objects.get(id=attrs.get('customer'))
            ad=attrs.get('account_details')
            #co=Method.objects.get(id=attrs.get('coin'))
            print(attrs.get('customer'))
            am=attrs.get('amount')
            trc=attrs.get('trc20_address')
            bep=attrs.get('bep20_address')
            me=attrs.get('method')

            order=Order.objects.create(
                customer=attrs.get('customer'),
                account_details=ad,
                coin=attrs.get('coin'),
                amount=am,
                purpose=None,
                trc20_address=trc,
                bep20_address=bep,
                method=me,

            )
            return order 
        
class AllOrdersSerializers(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields=['id','account_details', 'amount', 'method','state','time']