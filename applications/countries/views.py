from rest_framework import viewsets
from .models import Country
from .serializers import CountriesSerializer
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from permissions.permissions import IsNotBlocked, IsNotAdmin


class CountriesModelViewSet(viewsets.ModelViewSet):
    permission_classes = [
        DjangoModelPermissionsOrAnonReadOnly,
        IsNotBlocked,
        IsNotAdmin,
    ]
    queryset = Country.objects.all()
    serializer_class = CountriesSerializer
    pagination_class = None
