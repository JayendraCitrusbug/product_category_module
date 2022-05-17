from product_module.settings import *
import product_module.settings
import stripe
import datetime
from .serializers import *
from website.models import *
from rest_framework import status
from rest_framework import viewsets
from django.http import JsonResponse
from django.shortcuts import redirect
from .paginations import CustomPagination
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

stripe.api_key=STRIPE_SECRET_KEY

class UserModelViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = CustomPagination

    def list(self, request, *args, **kwargs):
        user = User.objects.all()
        search = request.GET.get('search')
        if search:
            user = user.filter(username__icontains=search)

        serializer = UserSerializer(user, many=True)
        return Response(serializer.data)


class CategoryModelViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = CustomPagination

    def list(self, request, *args, **kwargs):
        category = Category.objects.all()
        search = request.GET.get('search')
        if search:
            category = category.filter(category__icontains=search)

        serializer = CategorySerializer(category, many=True)
        return Response(serializer.data)


class ProductsModelViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer
    pagination_class = CustomPagination

    def list(self, request, *args, **kwargs):
        product = Products.objects.filter(isDelete=False)
        search = request.GET.get('search')
        filter = request.GET.get('filter')
        if search:
            product = product.filter(product_name__icontains=search)
        if filter:
            product = product.filter(category__category=filter)

        serializer = ProductsSerializer(product, many=True)
        return Response(serializer.data)

    def destroy(self, request, pk):
        product = Products.objects.get(id=pk)
        product.isDelete = True
        product.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CouponModelViewSet(viewsets.ModelViewSet):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    pagination_class = CustomPagination

    def list(self, request, *args, **kwargs):
        coupon = Coupon.objects.all()
        search = request.GET.get('search')
        if search:
            coupon = coupon.filter(name__icontains=search)

        serializer = CouponSerializer(coupon, many=True)
        return Response(serializer.data)


class PlanModelViewSet(viewsets.ModelViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
    pagination_class = CustomPagination
    authentication_classes = [JWTAuthentication]

    def list(self, request, *args, **kwargs):
        plan = Plan.objects.all()
        search = request.GET.get('search')
        if search:
            plan = plan.filter(name__icontains=search)

        serializer = PlanSerializer(plan, many=True)
        return Response(serializer.data)

    def create(self, request, **validate_data):
        plans = Plan.objects.filter(name=request.POST['name']).exists()
        if request.user.is_superuser:
            if plans:
                return Response("This plan already exists so add another plan...!")
            else:
                if request.data['days'] == "28":
                    interval = 'month'
                    count = 1
                if request.data['days'] == "168":
                    interval = 'month'
                    count = 6
                elif request.data['days'] == "365":
                    interval = 'year'
                    count = 1
                plan_create = Plan.objects.create(name=request.POST['name'], duration_days=request.POST['days'], price=request.POST['price'])
                stripe_plan = stripe.Product.create(name=request.POST['name'])
                stripe_price = stripe.Price.create(active=True, currency='inr', recurring={"interval": interval, "interval_count": count}, product=stripe_plan.id, unit_amount=int(request.POST['price'])*100)
                plan_create.stripe_product_id = stripe_plan.id
                plan_create.stripe_price_id = stripe_price.id
                plan_create.save()
                return Response(stripe_plan.id)
        else:
            return Response("Only admin can create plans...!")


class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    pagination_class = CustomPagination
    authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        subscription = Subscription.objects.all()
        search = request.GET.get('search')
        if search:
            subscription = subscription.filter(name__icontains=search)

        serializer = SubscriptionSerializer(subscription, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        if request.user.customer_id:
            stripe_customer_id = request.user.customer_id
        else:
            stripe_customer = stripe.Customer.create(name=request.user.username, email=request.user.email)
            stripe_customer_id = stripe_customer.id

        try:
            plan = Plan.objects.get(name=request.data["plan"])
            stripe_source = stripe.Customer.create_source(stripe_customer_id, source="tok_in")
            request.user.customer_id = stripe_customer_id
            request.user.save()
            try:
                stripe_subscription = stripe.Subscription.create(customer=stripe_customer_id, default_source=stripe_source.id, items=[{"price":plan.stripe_price_id}])
                model_subscription = Subscription.objects.create(username=request.user, stripe_subscription_id=stripe_subscription.id, payment_via=stripe_source.id, plan=plan)
            except:
                return Response("Already subscribed a plan...!")
        except:
            return Response("This plan doesn't exists...!")

        invoice = stripe.Invoice.retrieve(stripe_subscription.latest_invoice)
        payment_intent = stripe.PaymentIntent.retrieve(invoice.payment_intent)
        next_action_url = payment_intent.next_action.use_stripe_sdk.stripe_js
        link = {}
        link["authentication_url"] = next_action_url
        return Response(link)


import requests
# from allauth.socialaccount.models import SocialLogin
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

class SocialLoginViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        user = User.objects.all()
        search = request.GET.get('search')
        if search:
            user = user.filter(name__icontains=search)

        serializer = UserSerializer(user, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        token = request.data['token']
        req1 = requests.get(f"https://graph.facebook.com/v13.0/me?fields=email&access_token={token}")
        data = req1.json()
        email = data["email"]
        dict = {}
        dict["facebook_email"]=email
        return Response(dict)


import base64
class MiddlewareTokenViewSet(viewsets.ModelViewSet):
    def create(self, request, *args, **kwargs):
        user_id = request.data['user_id']
        user_password = User.objects.get(pk=user_id).password
        user_password_hasher = user_password.split("$")[3]
        time = datetime.datetime.now() + datetime.timedelta(days=1)
        string = str(user_id) + "$" + user_password_hasher + "$" + str(time)

        encoded_string_bytes = string.encode("ascii")
        encoded_base64_bytes = base64.b64encode(encoded_string_bytes)
        encoded_base64_string = encoded_base64_bytes.decode("ascii")

        data = {}
        # data['string'] = string
        data['encoded'] = encoded_base64_string
        # data['decoded'] = decoded_base64_string

        return Response(data)

