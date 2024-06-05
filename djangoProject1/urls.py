from django.contrib import admin
from django.urls import path
from main.views import main_page, callback_view
from account.views import (RegisterView, MyLoginView, logout_view, profile_view, manager_profile_view,
                           client_profile_view)


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

]
