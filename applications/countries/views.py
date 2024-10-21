from rest_framework import viewsets
from .models import Country
from .serializers import CountriesSerializer
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly


class CountriesModelViewSet(viewsets.ModelViewSet):
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    queryset = Country.objects.all()
    serializer_class = CountriesSerializer
    pagination_class = None
