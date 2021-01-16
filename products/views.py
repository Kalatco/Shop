from django.shortcuts import render
from django.conf import settings
from products.tasks import send_order_email
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from products.models import Product, Category, ProductSize, OrderProduct
from products.serializers import (
    ProductSerializer,
    OrderSerializer,
    CategorySerializer,
    OrderProductSerializer
)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    @action(methods=['GET'], detail=True)
    def products(self, request, pk=None):
        send_email.delay('celery task worked!')
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

        # Get data from database to prepare for email template and send to celery
        orderSerializer = serializer.data
        orderItems = OrderProduct.objects.filter(order=orderSerializer['id'])
        orderItemsSerializer = OrderProductSerializer(orderItems, many=True)

        orderItemsList = []
        totalCost = 0.0
        for item in orderItemsSerializer.data:
            temp = {}
            temp['name'] = Product.objects.get(pk=item['product']).name
            product_size = ProductSize.objects.get(pk=item['product_size'])
            temp['size'] = product_size.size.name
            temp['cost'] = product_size.cost
            temp['quantity'] = item['quantity']
            totalCost += (item['quantity'] * product_size.cost)
            orderItemsList.append(temp)
        send_order_email.delay(orderSerializer, orderItemsList, totalCost)
        return Response(status=status.HTTP_201_CREATED)

    @action(methods=['GET'], detail=False)
    def config(self, request):
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return Response(stripe_config)
