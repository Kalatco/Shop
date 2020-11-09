from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from products.models import Product
from products.serializers import (
    ProductSerializer,
    OrderSerializer
)


class ProductViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = ProductSerializer
    queryset = Product.objects.filter(is_visible=True)


class OrderViewSet(viewsets.ViewSet):

    @swagger_auto_schema(request_body=OrderSerializer)
    def create(self, request):
        serializer = OrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)
