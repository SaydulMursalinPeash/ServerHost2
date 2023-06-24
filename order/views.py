from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from payment.models import Method

class Order(APIView):
    permission_classes=[IsAuthenticated]
    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LatestUserOrder(APIView):
    permission_classes=[IsAuthenticated]
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
    def post(self,request,order_id):
        order=Order.objects.get(id=order_id)
        if not request.user.is_officer and not request.user.is_admin:
            return Response({'error':'You are not permitted to do this action.'},status=status.HTTP_400_BAD_REQUEST)
        state=request.data.get('state')
        order.state=state
        order.save()
        return Response({'msg':'Order state successfully changed to '+state+'.'},status=status.HTTP_200_OK)
    
class GetAllOrdersView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        if not request.user.is_admin and not request.user.is_officer:
            return Response({'error':'You are not permitted to do this action.'},status=status.HTTP_400_BAD_REQUEST)
        orders=Order.objects.all()
        serializer=OrderSerializer(orders,many=True)
        return Response({'msg':serializer.data,},status=status.HTTP_200_OK)
