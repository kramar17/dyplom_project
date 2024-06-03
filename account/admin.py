from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import OfferModel, DiscountModel, UserDiscount


@admin.register(OfferModel)
class OfferModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'old_price', 'eating_plan', 'free_consultation', 'back_up_money', 'couching',
                    'consultation_about_sport', 'free_week_for_family', 'sort', 'slug')
    list_editable = ('price', 'old_price', 'eating_plan','free_consultation', 'back_up_money', 'couching',
                     'consultation_about_sport', 'free_week_for_family', 'sort')
    prepopulated_fields = {"slug": ("name",)}


@admin.register(DiscountModel)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('name', 'percentage')


class UserDiscountInline(admin.TabularInline):
    model = UserDiscount
    extra = 1


class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'has_discount', 'discount_percentage', 'is_staff')

    def has_discount(self, obj):
        return obj.userdiscount.discount.name if hasattr(obj, 'userdiscount') and obj.userdiscount.discount else 'No Discount'

    def discount_percentage(self, obj):
        return obj.userdiscount.discount.percentage if hasattr(obj, 'userdiscount') and obj.userdiscount.discount else ''

    has_discount.short_description = 'Discount'
    discount_percentage.short_description = 'Discount Percentage'


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
