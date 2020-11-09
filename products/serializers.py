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
        fields = ['cost', 'size']


class ProductSerializer(serializers.ModelSerializer):
    images = ImageSerializer(read_only=True, many=True)
    sizes = ProductSizeSerializer(read_only=True, many=True)
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = ['images', 'name', 'description', 'category', 'sizes']


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = '__all__'


class CheckoutProductSizeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductSize
        fields = ['size']


class OrderProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderProduct
        fields = ['product', 'quantity', 'product_size']


class OrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    orderItems = OrderProductSerializer(many=True)

    class Meta:
        model = Order
        fields = ['customer', 'orderItems']

    def create(self, validated_data):
        customer_data = validated_data.pop('customer')
        order_items_data = validated_data.pop('orderItems')

        # Create user & order models
        customer = Customer.objects.create(**customer_data)
        order = Order.objects.create(customer=customer, **validated_data)

        # Create a model for each product ordered, if its quantity and product size is valid.
        for item_data in order_items_data:
            product_size_data = item_data.pop('product_size')
            
            if product_size_data.product != item_data['product']:
                raise serializers.ValidationError({'message': 'Invalid Product Size chosen'})

            if item_data['quantity'] <= 0:
                raise serializers.ValidationError({'message': 'Invalid Quantity, must be 1 or greater'})

            OrderProduct.objects.create(order=order, cost=product_size_data.cost, product_size=product_size_data, **item_data)

        return order
