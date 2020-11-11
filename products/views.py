from django.shortcuts import render
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from products.models import Product, Category
from products.serializers import (
    ProductSerializer,
    OrderSerializer,
    CategorySerializer
)



class CategoryViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    @action(methods=['GET'], detail=True)
    def products(self, request, pk=None):
        products = Product.objects.filter(category=pk)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


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

    @action(methods=['GET'], detail=False)
    def config(self, request):
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return Response(stripe_config)
