from django.contrib import admin
from .models import OfferModel


@admin.register(OfferModel)
class OfferModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'old_price', 'eating_plan', 'free_consultation', 'back_up_money', 'couching',
                    'consultation_about_sport', 'free_week_for_family', 'sort', 'slug')
    list_editable = ('price', 'old_price', 'eating_plan','free_consultation', 'back_up_money', 'couching',
                     'consultation_about_sport', 'free_week_for_family', 'sort')
    prepopulated_fields = {"slug": ("name",)}



