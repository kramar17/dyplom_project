from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from main.views import main_page, callback_view
from account.views import (RegisterView, MyLoginView, logout_view, profile_view, manager_profile_view,
                           client_profile_view)
from shop.views import OurShopView, AddToCartView


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
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
