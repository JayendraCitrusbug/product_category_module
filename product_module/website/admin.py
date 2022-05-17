from django.contrib import admin
from .models import *


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ['username', 'product_name','category', 'img', 'quantity', 'description', 'price', 'isDelete', 'id']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category']

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['name', 'discount_amount_in_percentage']

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'duration_days', 'stripe_product_id', 'stripe_price_id', 'price']

@admin.register(Subscription)
class SubsciptionAdmin(admin.ModelAdmin):
    list_display = ['username', 'stripe_subscription_id', 'payment_via', 'plan', 'plan_puchased_at', 'cancel_at_period_end', 'has_active_plan']

@admin.register(SellProducts)
class SellProductsAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity', 'total_price', 'date']