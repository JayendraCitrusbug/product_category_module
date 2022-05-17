from rest_framework import serializers
from website.models import *


# |<-----------------------------------------------------User Serializer------------------------------------------------------------->|
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validate_data):
        return super().update(instance, validate_data)



# |<--------------------------------------------------Category Serializer---------------------------------------------------------------->|
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

    def create(self, validate_data):
        return Category.objects.create(**validate_data)

    def update(self, instance, validate_data):
        return super().update(instance, validate_data)



# |<-------------------------------------------------------------Product Serializer------------------------------------------------------>|
class ProductsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only = True)
    username = serializers.CharField(max_length=70)
    product_name = serializers.CharField(max_length=70)
    category = serializers.CharField(max_length=70)
    img = serializers.ImageField()
    description = serializers.CharField(max_length=200)
    price = serializers.IntegerField()
    isDelete = serializers.BooleanField(default = False)
    class Meta:
        model = Products
        fields = "__all__"

    def create(self, validate_data):
        return Products.objects.create(**validate_data)

    def update(self, instance, validate_data):
        return super().update(instance, validate_data)



class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = "__all__"
    
    def create(self, validate_data):
        return Coupon.objects.create(**validate_data)

    def update(self, instance, validate_data):
        return super().update(instance, validate_data)



class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = "__all__"
    
    def create(self, validate_data):
        return Plan.objects.create(**validate_data)

    def update(self, instance, validate_data):
        return super().update(instance, validate_data)



class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"
    
    def create(self, validate_data):
        return Subscription.objects.create(**validate_data)

    def update(self, instance, validate_data):
        return super().update(instance, validate_data)



class TestSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=255)

    def to_representation(self, instance):
        fields_map = {
            "FirstName": "first_name",
            "first_name":"FirstName", 
        }

        for key, value in fields_map.items():
            instance[value] = instance.pop(key)
        return instance
