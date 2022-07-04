# from email.message import _PayloadType
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.urls import reverse
from rest_framework import generics, status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterUser, UserSerializer, EmailVerificatoinSerializer
from config.settings.local import SECRET_KEY
from config.settings.base import EMAIL_HOST 


import jwt

User = get_user_model()


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"

    # def get_queryset(self, *args, **kwargs):
    #     assert isinstance(self.request.user.id, int)
    #     return self.queryset

    @action(detail=False)
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class RegisterUsers(generics.GenericAPIView):

    serializer_class = RegisterUser

    def post(self, request):

        user = request.data
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data["email"])
        token = RefreshToken.for_user(user).access_token
        current_site = "0.0.0.0:8000"
        relative_link = reverse("api:verify-email")
        absurl = "http://" + current_site + relative_link + "?token=" + str(token)
        email_body = (
            "Hi "
            + user.name.split(" ")[0]
            + ",\n"
            + "Thank you for registering with us, Please use the link below to verify your email address \n"
            + absurl
        )
        email_subject = "Verify your email address"

        email = EmailMessage(subject=email_subject, body=email_body, to=[user.email])
        email.send()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class VerifyEmail(generics.GenericAPIView):
    serializer_class = EmailVerificatoinSerializer
    def get(self, request):
        token = request.GET.get('token')

        try:
            Payload =jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=Payload['user_id'])
            if not user.is_verified:
                user.is_verified=True
                user.save()
            return Response({'email':'Successfully Activated'}, status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError as identifier :
            return Response({'error':'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)

        except jwt.exceptions.DecodeError as identifier :
            return Response({'error':'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)
