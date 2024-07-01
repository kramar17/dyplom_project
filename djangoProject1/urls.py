from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from main.views import main_page, callback_view
from account.views import (RegisterView, MyLoginView, logout_view, profile_view, manager_profile_view,
                           client_profile_view)
from shop.views import (OurShopView, AddToCartView, CartView, PaymentView, PaymentSuccessView,
                        PaymentIsSuccessView, UpdateCartView, ProductDetailView, add_comment)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_page, name='index'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', MyLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),

    path('profile/', profile_view, name='profile'),
    path('callback/', callback_view, name='callback'),
    path('manager_profile/', manager_profile_view, name='manager_profile'),
    path('client/<int:client_id>/', client_profile_view, name='client_profile'),

    path('our_shop/', OurShopView.as_view(), name='our_shop'),
    path('add_to_cart/<int:product_id>/', AddToCartView.as_view(), name='add_to_cart'),
    path('our_shop/cart', CartView.as_view(), name='cart'),
    path('our_shop/payment/', PaymentView.as_view(), name='payment'),
    path('our_shop/payment/success/', PaymentSuccessView.as_view(), name='payment_success'),
    path('our_shop/payment/success_pay', PaymentIsSuccessView.as_view(), name='success_pay'),
    path('our_shop/update_cart/', UpdateCartView.as_view(), name='update_cart'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/<int:pk>/add_comment/', add_comment, name='add_comment'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
