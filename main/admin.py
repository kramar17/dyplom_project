from django.contrib import admin
from .models import CallBackModel


@admin.register(CallBackModel)
class CallBackModelAdmin(admin.ModelAdmin):
    """
    Admin configuration for CallBackModel.

    Attributes:
        list_display (tuple): Fields to display in the admin list view.
        list_editable (tuple): Editable fields in the admin list view.
        list_filter (tuple): Fields to filter by in the admin list view.
    """

    list_display = ('name', 'date', 'time', 'phone', 'is_confirmed')
    list_editable = ('is_confirmed',)
    list_filter = ('is_confirmed',)
