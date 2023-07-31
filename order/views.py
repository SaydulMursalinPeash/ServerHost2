from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from payment.models import Method
from accounts.renderers import *
from rest_framework.permissions import AllowAny
from django.core.exceptions import ObjectDoesNotExist
from accounts.models import AccessToken
class Order(APIView):
    permission_classes=[AllowAny]
    renderer_classes=[UserRenderer]
    def post(self, request,format=None):
        access_token = request.GET.get('access_token')
        token_user=None
        if access_token is None:
            return Response({'error':'Access token is required.'},status=status.HTTP_400_BAD_REQUEST)
        token_obj=None
        try:
            token_obj=AccessToken.objects.get(token=access_token)
        except ObjectDoesNotExist as e:
            return Response({'error':'Access token is not valid.'},status=status.HTTP_400_BAD_REQUEST)
        if token_obj is None:
            return Response({'error':'Access token is not valid.'},status=status.HTTP_400_BAD_REQUEST)
        
        token_user=token_obj.user
        if token_user.id is not request.data.get('customer') and not token_user.is_admin:
            return Response({'error':'You are not Allowed to do this action.'},status=status.HTTP_400_BAD_REQUEST)
        
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            #serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


'''
class Order(APIView):
    permission_classes=[IsAuthenticated]
    renderer_classes=[UserRenderer]
    def post(self, request,format=None):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            #serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
'''
class LatestUserOrder(APIView):
    permission_classes=[IsAuthenticated]
    renderer_classes=[UserRenderer]
    def get(self,request,user_uid,coin_id,format=None):
        user= User.objects.get(id=user_uid)
        method=Method.objects.get(id=coin_id)
        if not user==request.user and not request.user.is_admin and not request.user.is_officer:
            return Response({'error':'You are not permitted to do this action. Sorry!'},status=status.HTTP_400_BAD_REQUEST)
        latest_order=None
        try:
            latest_order = Order.objects.filter(customer=user,coin=method).latest('created_at')
        except Order.DoesNotExist:
            latest_order = None
        
        if latest_order is not None:
            serializer=OrderSerializer(latest_order)
            return Response({'msg':serializer.data,},status=status.HTTP_200_OK)
        return Response({'error':'No order found!'},status=status.HTTP_404_NOT_FOUND)


class EditOrderView(APIView):
    permission_classes=[IsAuthenticated]
    renderer_classes=[UserRenderer]
    def post(self,request,order_id,format=None):
        order=Order.objects.get(id=order_id)
        if not request.user.is_officer and not request.user.is_admin:
            return Response({'error':'You are not permitted to do this action.'},status=status.HTTP_400_BAD_REQUEST)
        state=request.data.get('state')
        order.state=state
        order.save()
        return Response({'msg':'Order state successfully changed to '+state+'.'},status=status.HTTP_200_OK)
    
class GetAllOrdersView(APIView):
    permission_classes=[IsAuthenticated]
    renderer_classes=[UserRenderer]
    def get(self,request):
        if not request.user.is_admin and not request.user.is_officer:
            return Response({'error':'You are not permitted to do this action.'},status=status.HTTP_400_BAD_REQUEST)
        orders=Order.objects.all()
        serializer=OrderSerializer(orders,many=True)
        return Response({'msg':serializer.data,},status=status.HTTP_200_OK)


class BuyOrder(APIView):
    permission_classes=[AllowAny]
    def post(self,request,format=None):
        access_token = request.GET.get('access_token')
        token_user=None
        if access_token is None:
            return Response({'error':'Access token is required.'},status=status.HTTP_400_BAD_REQUEST)
        token_obj=None
        try:
            token_obj=AccessToken.objects.get(token=access_token)
        except ObjectDoesNotExist as e:
            return Response({'error':'Access token is not valid.'},status=status.HTTP_400_BAD_REQUEST)
        if token_obj is None:
            return Response({'error':'Access token is not valid.'},status=status.HTTP_400_BAD_REQUEST)
        
        token_user=token_obj.user
        if token_user.id is not request.data.get('customer') and not token_user.is_admin:
            return Response({'error':'You are not Allowed to do this action.'},status=status.HTTP_400_BAD_REQUEST)
        
        serializer = BuyOrderSerializer(data=request.data)
        if serializer.is_valid():
            #serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SellOrder(APIView):
    permission_classes=[AllowAny]
    def post(self,request,format=None):
        access_token = request.GET.get('access_token')
        token_user=None
        if access_token is None:
            return Response({'error':'Access token is required.'},status=status.HTTP_400_BAD_REQUEST)
        token_obj=None
        try:
            token_obj=AccessToken.objects.get(token=access_token)
        except ObjectDoesNotExist as e:
            return Response({'error':'Access token is not valid.'},status=status.HTTP_400_BAD_REQUEST)
        if token_obj is None:
            return Response({'error':'Access token is not valid.'},status=status.HTTP_400_BAD_REQUEST)
        
        token_user=token_obj.user
        if token_user.id is not request.data.get('customer') and not token_user.is_admin:
            return Response({'error':'You are not Allowed to do this action.'},status=status.HTTP_400_BAD_REQUEST)
        
        serializer = SellOrderSerializer(data=request.data)
        if serializer.is_valid():
            #serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class OrderStateChange(APIView):
    permission_classes=[AllowAny]
    def put(self,request,id):
        access_token = request.GET.get('access_token')
        token_user=None
        if access_token is None:
            return Response({'error':'Access token is required.'},status=status.HTTP_400_BAD_REQUEST)
        token_obj=None
        try:
            token_obj=AccessToken.objects.get(token=access_token)
        except ObjectDoesNotExist as e:
            return Response({'error':'Access token is not valid.'},status=status.HTTP_400_BAD_REQUEST)
        if token_obj is None:
            return Response({'error':'Access token is not valid.'},status=status.HTTP_400_BAD_REQUEST)
        
        token_user=token_obj.user
        if token_user.id is not request.data.get('customer') and not token_user.is_admin:
            return Response({'error':'You are not Allowed to do this action.'},status=status.HTTP_400_BAD_REQUEST)
        try:
            order_obj=Order.objects.get(id=id)
        except ObjectDoesNotExist as e:
            return Response({'msg':'Invalid order Id.'},status=status.HTTP_200_OK)
        order_obj.state=True
        order_obj.save()
        return Response({'msg':'Order state changet to Completed successfully.'},status=status.HTTP_200_OK)