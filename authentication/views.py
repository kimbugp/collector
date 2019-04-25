from django.contrib.auth import login
from authentication.models import User
from django.http import Http404
from rest_framework import generics
from rest_framework.permissions import (AllowAny, DjangoModelPermissions,
                                        IsAuthenticated)
from rest_framework.response import Response
from social_django.utils import load_backend, load_strategy

from .serializer import SocialSerializer, UserSerializer


class SocialAuthView(generics.CreateAPIView):
    serializer_class = SocialSerializer

    def post(self, request, backend, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            strategy = load_strategy(request)
            request.backend = load_backend(strategy, backend, None)
            user = request.backend.do_auth(
                serializer.validated_data['access_token'])
        except Exception as e:
            return Response({"error": str(e)})
        if user:
            login(request, user)
            return Response({'email': user.email,
                             'username': user.username
                             })
        return Response({"error": "unknown login error"})

class UserView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = (DjangoModelPermissions,)
    queryset = User.objects.none()

    def get(self,request):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data)
