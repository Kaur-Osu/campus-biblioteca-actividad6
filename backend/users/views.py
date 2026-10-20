from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .models import User
from .serializers import UserSerializer, PublicUserSerializer
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
@method_decorator(name='list', decorator=swagger_auto_schema(responses={200:PublicUserSerializer(many=True)}))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(responses={200:PublicUserSerializer()}))
@method_decorator(name='create', decorator=swagger_auto_schema(responses={201:PublicUserSerializer()}))
@method_decorator(name='update', decorator=swagger_auto_schema(responses={200:PublicUserSerializer()}))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(responses={200:PublicUserSerializer()}))
class UserApiViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer
    queryset = User.objects.all().order_by('id')
class UserView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PublicUserSerializer
    def get_object(self):
        return self.request.user
