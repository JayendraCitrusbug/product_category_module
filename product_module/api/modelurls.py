from . import modelviews
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('modeluser', modelviews.UserModelViewSet, basename='modeluser')
router.register('modelcategory', modelviews.CategoryModelViewSet, basename='modelcategory')
router.register('modelproducts', modelviews.ProductsModelViewSet, basename='modelproducts')
router.register('modelcoupon', modelviews.CouponModelViewSet, basename='modelcoupon')
router.register('modelplan', modelviews.PlanModelViewSet, basename='modelplan')
router.register('modelsubscription', modelviews.SubscriptionViewSet, basename='modelsubscription')
router.register('modelsociallogin', modelviews.SocialLoginViewSet, basename='modelsociallogin')
router.register('middlewaretoken', modelviews.MiddlewareTokenViewSet, basename='middlewaretoken')

urlpatterns = [
    path('', include(router.urls)),
    # path('gettoken/', CustomAuthToken.as_view()),
]