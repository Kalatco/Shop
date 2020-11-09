from django.db import models
from django.utils.html import mark_safe


class Category(models.Model):
    name = models.TextField(max_length=50)

    def __str__(self):
        return self.name


class Size(models.Model):
    name = models.TextField(max_length=50)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.TextField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField(max_length=300)
    is_visible = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ProductSize(models.Model):
    product = models.ForeignKey(Product, related_name='sizes', on_delete=models.CASCADE, null=True)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    cost = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.size}"


class Image(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')
    primary = models.BooleanField(default=False)

    @property
    def image_preview(self):
        if self.image:
            return mark_safe(f'<image src="{self.image.url}" width="300" height="200" />')
        return ""


class Customer(models.Model):
    first_name = models.TextField(max_length=120)
    last_name = models.TextField(max_length=120)
    email = models.TextField(max_length=120)
    address = models.TextField(max_length=120)
    appartment = models.TextField(max_length=120, default=None, blank=True, null=True)
    city = models.TextField(max_length=120)
    state = models.TextField(max_length=120, default=None, blank=True, null=True)
    country = models.TextField(max_length=120)
    zip_code = models.TextField(max_length=120, default=None, blank=True, null=True)
    phone = models.TextField(max_length=120, default=None, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Order(models.Model):
    ORDER_STATUS = [
        (0, 'In progress'),
        (1, 'Shipping'),
        (2, 'Delivered'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    status = models.PositiveSmallIntegerField(
        choices=ORDER_STATUS,
        default=0
    )
    tracking = models.TextField(max_length=120, default=None, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def customer_first_name(self):
        return f"{self.customer.first_name} {self.customer.last_name}"
    customer_first_name.short_description = 'Customer'

    def customer_email(self):
        return self.customer.email
    customer_email.short_description = 'Email'

    def customer_address(self):
        return f"{self.customer.address} {self.customer.appartment} \n \
               {self.customer.city}, {self.customer.city}, {self.customer.country} \n \
               {self.customer.zip_code}"
    customer_address.short_description = 'Address'

    def customer_phone(self):
        return self.customer.phone
    customer_phone.short_description = 'Phone number'
    

class OrderProduct(models.Model):
    product = models.ForeignKey(Product, related_name='orderItems', on_delete=models.CASCADE)
    product_size = models.ForeignKey(ProductSize, related_name='productSize', on_delete=models.CASCADE, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    cost = models.FloatField(default=0.0)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def total_cost(self):
        return self.cost*self.quantity
