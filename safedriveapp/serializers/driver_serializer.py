from rest_framework import serializers
from safedriveapp.models import Driver
from safedriveapp.serializers.user_serializer import UserSerializer


class DriverSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(instance='user', read_only=True)

    """
    profiles - Hyperlinked relationship between DriverModel and Profiles model(
            driver serves as "foreign key" in the profile model)
    driver_data - Hyperlinked relationship between DrivingData and Driver (driver
            serves as the identity fields in the data_driver model)
    """
    class Meta:
        model = Driver
        fields = ('id', 'user', 'name', 'creation_date', 'driving_data')
