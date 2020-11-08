from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from products.models import Product
from products.serializers import (
    ProductSerializer
)


class ProductViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = ProductSerializer
    queryset = Product.objects.filter(is_visible=True)
