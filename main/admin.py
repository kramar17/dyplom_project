from django.contrib import admin
from .models import CallBackModel


@admin.register(CallBackModel)
class CallBackModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'time', 'phone', 'is_confirmed')
    list_editable = ('is_confirmed',)
    list_filter = ('is_confirmed',)
