from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework_extensions import mixins
from rest_framework.decorators import detail_route
from django.contrib.auth.models import User
from safedriveapp.serializers.user_serializer import UserSerializer
from safedriveapp.models import Driver


class UserViewSet(viewsets.ModelViewSet, mixins.NestedViewSetMixin):
    """
    ViewSet for User
    NestedViewSetMixin is an Extension for DRF - makes possible to send simple
        post/get requests.
    """
    queryset = User.objects.filter(is_staff=False, is_superuser=False)
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                driver_name = request.data.pop('name')[0]
                user = serializer.save()
                driver = Driver(name=driver_name, user=user).save()
                return Response({'driver_id': driver.pk, 'user_id': user.pk}, status=status.HTTP_201_CREATED)
            else:
                return Response('User creation failed, make sure that user does not already exist', status=status.HTTP_400_BAD_REQUEST)
        except KeyError, IndexError:
            return Response('driver name is missing', status=status.HTTP_400_BAD_REQUEST)

