import stripe
from django.db import models
from django.contrib.auth.models import User
# from s3direct.fields import S3DirectField

class Category(models.Model):
    category = models.CharField(max_length=70, null=True, blank=True)
    
    def __str__(self):
        return self.category

class Products(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product_name = models.CharField(max_length=70)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    img = models.ImageField(upload_to = 'images/')
    quantity = models.IntegerField(default=5)
    # img = S3DirectField(dest="destination")
    description = models.TextField()
    price = models.PositiveIntegerField()
    isDelete = models.BooleanField(default = False)

    def __str__(self):
        return self.product_name

class Coupon(models.Model):
    name = models.CharField(max_length=255)
    discount_amount_in_percentage = models.IntegerField()

    def __str__(self):
        return self.name

class Plan(models.Model):
    name = models.CharField(max_length=255)
    duration_days = models.IntegerField()
    price = models.IntegerField()
    stripe_product_id = models.CharField(max_length=255, blank=True)
    stripe_price_id = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name

class Subscription(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    stripe_subscription_id = models.CharField(max_length=255)
    payment_via = models.CharField(max_length=255)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    plan_puchased_at = models.DateTimeField(auto_now_add=True)
    cancel_at_period_end = models.BooleanField(default=True)
    has_active_plan = models.BooleanField(default=True)

    def __str__(self):
        return self.username.username
        
class SellProducts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_price = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.product_name