from rest_framework import viewsets, status
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework_extensions import mixins
from safedriveapp.models import DataDriver
from safedriveapp.serializers.data_driver_serializer import DataDriverSerializer

COLUMNS_TO_CONVERT = ['rpm', 'throttle', 'accelerator', 'rpm', 'speed']


class DataDriverViewSet(viewsets.ModelViewSet, mixins.NestedViewSetMixin):
    """
    ViewSet for DataDriver 
    NestedViewSetMixin is an Extension for DRF - makes possible to send simple
        post/get requests.
    """
    queryset = DataDriver.objects.all()
    serializer_class = DataDriverSerializer

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        ride = request.query_params.get('ride', None)
        data_unit = request.query_params.get('data_unit', None)
        if ride is not None and len(obj) > 0:
            data = obj[int(ride)][int(data_unit)] if data_unit is not None else obj[int(ride)]
            return Response(data, status=status.HTTP_200_OK)
        else:
            return super(DataDriverViewSet, self).retrieve(request, *args, **kwargs)

    @detail_route(methods=['GET'])
    def len(self, request, *args, **kwargs):
        driving_data = self.get_object()
        return Response({'number of rides': len(driving_data),
                         'number of data units': sum(len(ride) for ride in driving_data)}, status=status.HTTP_200_OK)

