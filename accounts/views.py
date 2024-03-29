from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import *
from django.contrib.auth import authenticate
from .renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from django.utils.encoding import smart_str,force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .utils import Util
from .models import AccessToken
import django
django.setup()

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }



class UserRegistrationView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,format=None):
        serializer=UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user=serializer.save()
            token=get_tokens_for_user(user)
            token_gen2=PasswordResetTokenGenerator()
            token2=token_gen2.make_token(user)
            uid=smart_str(urlsafe_base64_encode(force_bytes(user.id)))
            link='https://ptopuser-h2u4.vercel.app/api/user/varify-email/'+uid+'/'+token2+'/'
            print('Email varify link: ',link)
            data={
                'subject':'Email varification.',
                'body':'Click following link to varify given email: '+link,
                'to_email':user.email
            }
            Util.send_email(data)
            return Response({'token':token,'msg':'Account created successfully.Please check your inbox to varify your email.'},status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class UserEmailVarificationView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,uid,token,format=None):
        serializer=UserEmailVarificationSerializer(data=request.data,context={'uid':uid,'token':token})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Email varified successfully.'},status=status.HTTP_200_OK)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST) 


class UserLoginView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,fromat=None):
        serializer=UserLoginSerializer(data=request.data)
        #print(serializer.is_valid())
        if serializer.is_valid(raise_exception=True):
            email=serializer.data.get('email')
            test_user=User.objects.get(email=email)
            if not test_user.is_valid:
                token_gen2=PasswordResetTokenGenerator()
                token2=token_gen2.make_token(test_user)
                uid=smart_str(urlsafe_base64_encode(force_bytes(test_user.id)))
                link='https://ptopuser-h2u4.vercel.app/api/user/varify-email/'+uid+'/'+token2+'/'
                print('Email varify link: ',link)
                data={
                    'subject':'Email varification.',
                    'body':'Click following link to varify given email: '+link,
                    'to_email':email
                }
                Util.send_email(data)
                return Response({'error':'Your account is Not Valid. Please check your Email to verify your account.'},status=status.HTTP_400_BAD_REQUEST)

            password=serializer.data.get('password')
            user=authenticate(email=email,password=password)
            user_ser=UserProfileSerializer(user)
            if user is not None:
                token2=get_tokens_for_user(user)
                print(token2['access'])
                AccessToken.objects.create(token=token2['access'],type='ACCESS',user=user)
                return Response({'token':token2,'profile_data':user_ser.data,'msg':'Login Successfull.'},status=status.HTTP_200_OK)
            else:
                return Response({'errors':{'non_field_errors':['Email or password is  not valid.']}},status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class UserProfileView(APIView):
    renderer_classes=[UserRenderer]
    permission_classes=[IsAuthenticated]
    def get(self,request,format=None):
        serializer=UserProfileSerializer(request.user)
        return Response(serializer.data,status=status.HTTP_200_OK)

 

class UserChangePasswordView(APIView):
    renderer_classes=[UserRenderer]
    permission_classes=[IsAuthenticated]

    def post(self,request,format=None):

        serializer=UserChangePasswordSerializer(data=request.data,context={'user':request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password changed successfully.'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class SendPasswordResetEmailView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,format=None):
        serializer=SendPasswordResetEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password reset email send.Please check your Inbox.'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)




class UserPasswordResetView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,uid,token,format=None):
        serializer=UserPasswordResetSerializer(data=request.data,context={'uid':uid,'token':token})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password reset successfully.'},status=status.HTTP_200_OK)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)


