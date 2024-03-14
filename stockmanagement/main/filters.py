import django_filters
from .models import *


class SaleFilter(django_filters.FilterSet):
    class Meta:
        models = Sale
        fields = ['qty']
