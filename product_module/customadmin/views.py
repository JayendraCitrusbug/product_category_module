from re import template
from sre_constants import SUCCESS
from django.contrib.auth.models import User, auth
from django.shortcuts import render, redirect
from django.views import View
from website.models import *
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.edit import UpdateView
from django.contrib import messages


# |<--------------------------------Home----------------------------->|
class CustomadminHomeView(View):
    def get(self, request):
        if request.user.is_authenticated and request.user.is_superuser:
            superuser = User.objects.filter(is_superuser=True)
            user_count = User.objects.all().count()
            category_count = Category.objects.all().count()
            product_count = Products.objects.all().count()
            context = {'superuser': superuser, 'user_count':user_count, 'category_count':category_count, 'product_count':product_count}
            return render(request, 'customadmin/home.html', context)
        else:
            return redirect('customadminlogin')

class CustomadminLoginView(View):
    def get(self, request):
            return render(request, 'customadmin/customadminlogin.html')
    
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('customadminhome/')
        else:
            messages.info(request, 'Invalid credentials !')
            return render(request, 'customadmin/customadminlogin.html')

class CustomadminLogoutView(View):
    def get(self, request):
        auth.logout(request)
        return redirect('customadminlogin')




# |<--------------------------------Users----------------------------->|
class UsersView(View):
    def get(self, request):
        superuser = User.objects.filter(is_superuser=True)
        user = User.objects.all().order_by('id')
        return render(request, 'customadmin/users/users.html', {'superuser': superuser, 'user': user})  

class UserAddView(CreateView):
    model = User
    fields = ['username', 'first_name', 'last_name', 'email', 'password']
    template_name = "customadmin/users/edituser.html"
    success_url = "/customadmin/users/"

class UserEditView(UpdateView):
    model = User
    fields = ['username', 'email', 'first_name', 'last_name']
    template_name = "customadmin/users/edituser.html"
    success_url = "/customadmin/users/"

class UserDeleteView(View):
    def get(self, request, id):
        user = User.objects.filter(id=id)
        user.delete()
        return redirect('users')



# |<--------------------------------Category----------------------------->|
class CategoryView(View):
    def get(self, request):
        category = Category.objects.all().order_by('id')
        superuser = User.objects.filter(is_superuser=True)
        return render(request, 'customadmin/category/category.html', {'category': category, 'superuser': superuser})

class CategoryAddView(CreateView):
    model = Category
    fields = ['category']
    template_name = "customadmin/category/editcategory.html"
    success_url = "/customadmin/category/"

class CategoryEditView(UpdateView):
    model = Category
    fields = ['category']
    template_name = "customadmin/category/editcategory.html"
    success_url = "/customadmin/category/"

class CategoryDeleteView(View):
    def get(self, request, id):
        category = Category.objects.filter(id=id)
        category.delete()
        return redirect('category')



# |<--------------------------------Products----------------------------->|
class ProductsView(View):
    def get(self, request):
        products = Products.objects.all().order_by('id')
        superuser = User.objects.filter(is_superuser=True)
        return render(request, 'customadmin/products/products.html', {'products': products, 'superuser': superuser})

class ProductsAddView(CreateView):
    model = Products
    fields = ['username', 'product_name', 'category', 'img', 'description', 'price']
    template_name = "customadmin/products/editproducts.html"
    success_url = "/customadmin/products/"

class ProductsEditView(UpdateView):
    model = Products
    fields = ['product_name', 'category', 'img', 'description', 'price']
    template_name = "customadmin/products/editproducts.html"
    products = Products.objects.all()
    success_url = "/customadmin/products/"

class ProductsDeleteView(View):
    def get(self, request, id):
        product = Products.objects.filter(id=id)
        product.delete()
        return redirect('products')
