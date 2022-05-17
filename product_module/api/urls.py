from django.urls import path, include

from allauth.socialaccount.providers.oauth2.views import OAuth2CallbackView
from .adapters import GoogleOAuth2AdapterIdToken
from .views import GoogleLoginView

from . import views

urlpatterns = [

# |<------------------------------------------------------------------------User------------------------------------------------------------------------------------------------------->|
    
    path('user/list/', views.UserAPI.as_view(), name="list"),
    path('user/details/<int:id>/', views.UserAPI.as_view(), name="details"),

# |<------------------------------------------------------------------------Category------------------------------------------------------------------------------------------------------->|

    path('category/list/', views.CategoryAPI.as_view(), name="list"),
    path('category/details/<int:id>/', views.CategoryAPI.as_view(), name="details"),

# |<------------------------------------------------------------------------Product------------------------------------------------------------------------------------------------------->|

    path('product/list/', views.ProductsAPI.as_view(), name="productslist"),
    path('product/details/<int:id>/', views.ProductsAPI.as_view(), name="productdetails"),

# |<------------------------------------------------------------------------Social Login------------------------------------------------------------------------------------------------------->|

    path("login/google/", GoogleLoginView.as_view(), name="google_login"),
    path("login/google/callback/", OAuth2CallbackView.adapter_view(GoogleOAuth2AdapterIdToken), name="google_callback"),

    path('test/', views.TestAPI.as_view(), name="test"),
]
