from requests import request
from .serializers import *
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter
from django.core.paginator import Paginator
from django.views import View
from website.models import *
from .serializers import *
import stripe


# Create your views here.

# |<------------------------------------------------------------------------User API---------------------------------------------------------------------------------------------------->|
class UserAPI(ListAPIView):
    def get(self, request, id=None):
        if id is not None:
            try:
                user = User.objects.get(id=id)
                serializer = UserSerializer(user)
            except:
                return JsonResponse("User details of this ID does not exist...!", safe=False)
        else:
            user = User.objects.all()
            search = request.GET.get('search')
            filter = request.GET.get('filter')

            if search:
                user = user.filter(username__icontains=search)
            if not user:
                return JsonResponse("No user found...!", safe=False)

            serializer = UserSerializer(user, many=True)
        return JsonResponse(serializer.data, safe=False)

    @csrf_exempt
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        else:
            return JsonResponse(serializer.errors)

    def patch(self, request, id):
        user = User.objects.get(id=id)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        else:
            return JsonResponse(serializer.errors)

    def delete(self, request, id):
        user = User.objects.get(id=id)
        user.delete()
        return JsonResponse("User Deleted", safe=False)


# |<------------------------------------------------------------------------Category API------------------------------------------------------------------------------------------------->|
class CategoryAPI(ListAPIView):
    def get(self, request, id=None):
        if id is not None:
            try:
                category = Category.objects.get(id=id)
                serializer = CategorySerializer(category)
            except:
                return JsonResponse("Category details of this ID does not exist...!", safe=False)
        else:
            category = Category.objects.all()
            search = request.GET.get('search')

            if search:
                category = category.filter(category__icontains=search)
            serializer = CategorySerializer(category, many=True)
        return JsonResponse(serializer.data, safe=False)

    @csrf_exempt
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        else:
            return JsonResponse(serializer.errors)

    def patch(self, request, id):
        category = Category.objects.get(id=id)
        serializer = CategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        else:
            return JsonResponse(serializer.errors)

    def delete(self, request, id):
        category = Category.objects.get(id=id)
        category.delete()
        return JsonResponse("Category Deleted", safe=False)


# |<------------------------------------------------------------------------Product API------------------------------------------------------------------------------------------------->|
class ProductsAPI(ListAPIView):

    def get(self, request, id=None):
        search = request.GET.get('search')
        filter = request.GET.get('filter')
        # page_size = 2
        page = request.GET.get('page')
        # page_size = request.GET.get('page_size')
        if id is not None:
            try:
                pro = Products.objects.get(id=id)
                serializer = ProductsSerializer(pro)
            except:
                return JsonResponse("Product details of this ID does not exist.....!", safe=False)
        else:
            product = Products.objects.filter(isDelete=False) 

            if search:
                product = product.filter(product_name__icontains=search)
            if filter:
                product = product.filter(category__category__icontains=filter)

            paginator = Paginator(product, 2)
            product = paginator.get_page(page)
            serializer = ProductsSerializer(product, many=True)
        return JsonResponse(serializer.data, safe=False)

    @csrf_exempt
    def post(self, request):
        serializer = ProductsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        else:
            return JsonResponse(serializer.errors)

    def patch(self, request, id):
        product = Products.objects.get(id=id)
        serializer = ProductsSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        else:
            return JsonResponse(serializer.errors)

    def delete(self, request, id):
        product = Products.objects.get(id=id)
        product.isDelete = True
        product.save()
        return JsonResponse("Product Deleted", safe=False)



# class CreateCheckoutSesionAPI(ListAPIView):
#     def post(self, request, *args, **kwargs):
#         checkout_session = stripe.checkout.Session.create(
#             line_items=[
#                 {
#                     'price_data': '{{PRICE_ID}}',
#                     'quantity': 1,
#                 },
#             ],
#             mode='payment',
#             success_url=YOUR_DOMAIN + '/success.html',
#             cancel_url=YOUR_DOMAIN + '/cancel.html',
#         )


from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from rest_auth.registration.serializers import SocialLoginSerializer
from rest_auth.registration.views import SocialLoginView
from api.adapters import GoogleOAuth2AdapterIdToken


class GoogleLoginView(SocialLoginView):
    adapter_class = GoogleOAuth2AdapterIdToken
    serializer_class = SocialLoginSerializer
    callback_url = "http://localhost:8000/api/v1/users/login/google/callback/"



class TestAPI(ListAPIView):
    def post(self, request):
        serializer = TestSerializer(request.data)
        return Response(serializer.data)