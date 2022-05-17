from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('s3direct/', include('s3direct.urls')),
    path("login", views.LoginView.as_view(), name="login"),
    path('', views.MainView.as_view(), name="home"),
    path("signup/", views.SignupView.as_view(), name="signup"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path('myproducts/', views.MyProductsView.as_view(), name="myproducts"),
    path('addproduct/', views.AddProductView.as_view(), name="add"),
    path('addcategory/', views.AddCategoryView.as_view(), name="addcategory"),
    path('catfilter/<int:pk>/', views.CatFilterView.as_view(), name="catfilter"),
    path('updateproduct/<int:pk>/', views.UpdateProductView.as_view(), name="update"),
    path('delete/<int:id>/', views.DeleteView.as_view(), name="delete"),
    path('readmore/<int:id>/', views.ReadMoreView.as_view(), name="readmore"),
    path('search/', views.SearchView.as_view(), name="search"),
    path('profile/<int:id>/', views.ProfileView.as_view(), name="profile"),
    path('checkout/<int:id>/', views.CheckoutView.as_view(), name="checkout"),
    path('buynow/<int:id>/', views.BuyNowView.as_view(), name="buynow"),
    # path('categoryfilter/', views.CategoryFilter, name="categoryfilter"),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
