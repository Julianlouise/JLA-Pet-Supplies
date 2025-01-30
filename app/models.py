from django.contrib.auth.models import User
from django.db import models
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Item(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, related_name='item', on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='item_images/', null=True, blank=True)

    def __str__(self):
        return self.title

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.TextField()
    contact = models.CharField(max_length=11)
    order_date = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    
    def __str__(self):
        return self.first_name

class OrderItem(models.Model):
    ordered = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models. DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Item{self.item_id} in Order {self.ordered.id}"