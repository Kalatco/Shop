from rest_framework import serializers
from products.models import (
    Category,
    Product,
    Image,
    Customer,
    Order,
    OrderProduct,
    ProductSize,
    Size
)


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ['image', 'primary']


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['name', 'id']


class SizeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Size
        fields = '__all__'


class ProductSizeSerializer(serializers.ModelSerializer):
    size = SizeSerializer()

    class Meta:
        model = ProductSize
        fields = ['price', 'size']


class ProductSerializer(serializers.ModelSerializer):
    images = ImageSerializer(read_only=True, many=True)
    sizes = ProductSizeSerializer(read_only=True, many=True)
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = ['images', 'name', 'description', 'category', 'sizes']
