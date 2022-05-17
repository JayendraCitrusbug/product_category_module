from email.mime import image
from multiprocessing import context
from this import d
from unicodedata import category
from django import views
from django.shortcuts import redirect, render
from django.contrib.auth.models import User, auth
from django.views import View
from django.views.generic.edit import UpdateView
from django.contrib import messages
from .models import Coupon, Products, Category, SellProducts
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.core import serializers
import json
from django.db.models import Q
import stripe
from product_module import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

class MainView(View):
    def get(self, request):
        if request.user.is_authenticated:
            soft_pro = Products.objects.filter(isDelete=False).order_by('-id')
            paginator = Paginator(soft_pro, 6, orphans=2)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            cat = Category.objects.all()
            return render(request, 'main/main.html', {'page_obj': page_obj, 'cat': cat, 'count_product': soft_pro.count})
        else:
            return redirect('login')


class LoginView(View):
    def get(self, request):
        return render(request, 'forms/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Invalid credentials !')
            return render(request, 'forms/login.html')


class SignupView(View):
    def get(self, request):
        return render(request, 'forms/signup.html')

    def post(self, request):
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username already exists')
                return render(request, 'forms/signup.html')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email already exists')
                return render(request, 'forms/signup.html')
            else:
                user = User.objects.create_user(
                    username=username, first_name=first_name, last_name=last_name, email=email, password=password1)
                user.save()
                return redirect('login')
        else:
            return render(request, 'forms/signup.html')


class LogoutView(View):
    def get(self, request):
        auth.logout(request)
        return redirect('login')


class MyProductsView(View):
    def get(self, request):
        if request.user.is_authenticated:
            cat = Category.objects.all()
            if request.user.is_superuser:
                mypro = Products.objects.filter(isDelete=False).order_by('-id')
                cat2 = [i.category for i in mypro]
                ci = request.GET.get("category")
                if ci:
                    mypro = Products.objects.filter(category=ci)
            else:
                mypro = Products.objects.filter(username=request.user, isDelete=False).order_by('-id')
                cat2 = [i.category for i in mypro]
                ci = request.GET.get("category")
                if ci:
                    mypro = Products.objects.filter(category=ci)
            mypro_counts = mypro.count()
            return render(request, 'my_products/myproducts.html', {'mypro': mypro, 'mypro_counts': mypro_counts, 'cat2': set(cat2), 'cat': cat})
        else:
            return redirect('login')


class AddProductView(View):
    def get(self, request):
        if request.user.is_authenticated:
            cat = Category.objects.all()
            return render(request, 'my_products/add.html', {'cat': cat})
        else:
            return redirect('login')

    def post(self, request):
        username = request.POST.get('un')
        pname = request.POST['pname']
        category = request.POST['category']
        category_object = Category.objects.get(category=category)
        img = request.FILES['img']
        desc = request.POST['description']
        price = request.POST['price']
        product = Products(product_name=pname, img=img, description=desc,
                           price=price, username=request.user, category=category_object)
        product.save()
        return redirect('myproducts')


class AddCategoryView(View):
    def get(self, request):
        if request.user.is_authenticated:
            cat = Category.objects.all()
            return render(request, 'my_products/addcategory.html', {'cat': cat})
        else:
            return redirect('login')

    def post(self, request):
        if request.user.is_authenticated:
            category = request.POST['category']
            category = category.lower()
            c = Category.objects.filter(category=category)
            if not c.exists():
                cat = Category(category=category)
                cat.save()
                return redirect('add')
            else:
                messages.info(request, 'This category already exists !')
                return redirect('addcategory')
        else:
            return redirect('login')


class CatFilterView(View):
    def get(self, request, pk):
        if request.user.is_authenticated:
            pro = Products.objects
            mypro = pro.filter(username=request.user).order_by('-id')
            cf = pro.filter(category=pk)
            cat = Category.objects.all()
            return render(request, 'my_products/catfilter.html', {'cf': cf, 'cat': cat, 'mypro': mypro})
        else:
            return redirect('login')


class UpdateProductView(UpdateView):
    model = Products
    fields = ['product_name', 'category', 'img', 'description', 'price']
    template_name = "my_products/update.html"
    mypro = Products.objects.filter(isDelete=False)
    cat = Category.objects.all()
    success_url = "/myproducts/"

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    context = {}

    def get_context_data(self, *args, **kwargs):
        context = super(UpdateProductView, self).get_context_data(
            *args, **kwargs)
        context['mypro'] = Products.objects.all()
        context['cat'] = self.cat
        return context


class DeleteView(View):
    def post(self, request, id):
        if request.user.is_authenticated:
            pi = Products.objects.get(pk=id)
            pi.isDelete = True
            pi.save()
            return redirect('myproducts')
        else:
            return redirect('login')


class ReadMoreView(View):
    def get(self, request, id):
        if request.user.is_authenticated:
            readproduct = Products.objects.filter(id=id).all()
            cat = Category.objects.all()
            return render(request, 'my_products/readmore.html', {'readproduct': readproduct, 'cat': cat})
        else:
            return redirect('login')


# class SearchView(View):
#     def get(self, request):
#         if request.user.is_authenticated:
#             search = request.GET.get('search')
#             result = Products.objects.filter(product_name__icontains=search)
#             return render(request, 'my_products/search.html', {'search': search, 'result': result})
#         else:
#             return redirect('login')


class ProfileView(View):
    def get(self, request, id):
        myprofile = Products.objects.filter(username=request.user)
        return render(request, 'my_products/profile.html', {'myprofile': myprofile})


# def CategoryFilter(request):
#     l = list()
#     all = Products.objects.all()
#     for i in all:
#         ser = CategorySerializer(i)
#         l.append(ser.data)
#     return HttpResponse(json.dumps(l))

class SearchView(View):
    def get(self, request):
        category_menu = Category.objects.all()
        searched = request.GET.get('search')
        product_searched = Products.objects.filter(Q(product_name__icontains=searched) | Q(
            description__icontains=searched) | Q(price__icontains=searched), isDelete=False)
        product_searched_json = serializers.serialize('json', product_searched)
        count_product = product_searched.count()
        # data = {
        #     # 'searched':searched,
        #     'product_searched':product_searched_json,
        #     # 'category_menu':category_menu,
        #     # 'count_product':count_product
        #     }
        # return render(request, 'searchproduct.html', data)
        return JsonResponse(product_searched_json, safe=False)


class CheckoutView(View):
    def get(self, request, id):
        if request.user.is_authenticated:
            pro = Products.objects.filter(id=id)
            coupons = Coupon.objects.all()
            key = settings.STRIPE_PUBLISHABLE_KEY
            for i in pro:
                amount = i.price

            verifycoupon = Coupon.objects.filter(name=request.GET.get('verify_coupon'))
            if verifycoupon:
                for i in verifycoupon:
                    coupon_name = i.name
                    discount = i.discount_amount_in_percentage
                coupon = coupon_name
                original_amt = amount
                coupen_amt = (discount*amount)/100
                final_amt = original_amt-coupen_amt
            else:
                coupon = 'none'
                original_amt = amount
                coupen_amt = 0
                final_amt = amount

            context = {'pro': pro, 'key': key,'coupon':coupon, 'original_amt': original_amt, 'final_amt': final_amt, 'stripeprice': final_amt*100}
            return render(request, "checkout.html", context)
        else:
            return redirect('login')

    def post(self, request, id):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return redirect('login')


class BuyNowView(View):
    def get(self, request, id):
        if request.user.is_authenticated:
            pro = Products.objects.filter(id=id)
            return render(request, "checkout.html", {'pro':pro})
        else:
            return redirect('login')

    def post(self, request, id):
        quantity = request.POST['quantity']
        total_price = request.POST['total_price']
        product = Products.objects.get(pk=id)
        sellproduct = SellProducts.objects.create(user=request.user, product=product, quantity=quantity[0], total_price=total_price)
        return redirect('home')

