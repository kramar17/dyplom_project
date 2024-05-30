from django.contrib import admin
from django.urls import path
from main.views import main_page
from account.views import RegisterView, MyLoginView, logout_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_page, name='index'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', MyLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
]
