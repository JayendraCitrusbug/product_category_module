from unicodedata import name
from django.urls import path
from customadmin import views

urlpatterns = [
# |<--------------------------------Home----------------------------->|
    path("", views.CustomadminLoginView.as_view(), name="customadminlogin"),
    path("customadminhome/", views.CustomadminHomeView.as_view(), name="customadminhome"),
    path("customadminlogout/", views.CustomadminLogoutView.as_view(), name="customadminlogout"),



# |<--------------------------------Users----------------------------->|
    path("users/", views.UsersView.as_view(), name="users"),
    path("user_add/", views.UserAddView.as_view(), name="useradd"),
    path("user_edit/<int:pk>/", views.UserEditView.as_view(), name="useredit"),
    path("user_delete/<int:id>/", views.UserDeleteView.as_view(), name="userdelete"),



# |<--------------------------------Category----------------------------->|
    path("category/", views.CategoryView.as_view(), name="category"),
    path("category_add/", views.CategoryAddView.as_view(), name="categoryadd"),
    path("category_edit/<int:pk>/", views.CategoryEditView.as_view(), name="categoryedit"),
    path("category_delete/<int:id>/", views.CategoryDeleteView.as_view(), name="categorydelete"),



# |<--------------------------------Products----------------------------->|
    path("products/", views.ProductsView.as_view(), name="products"),
    path("product_add/", views.ProductsAddView.as_view(), name="productadd"),
    path("product_edit/<int:pk>/", views.ProductsEditView.as_view(), name="productedit"),
    path("product_delete/<int:id>/", views.ProductsDeleteView.as_view(), name="productdelete"),
]
