from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import OfferModel, DiscountModel, UserDiscount, DietitianClient


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
    inlines = (UserDiscountInline,)
    list_display = ('username', 'first_name', 'last_name', 'has_discount', 'discount_percentage', 'is_staff')

    def has_discount(self, obj):
        if hasattr(obj, 'userdiscount') and obj.userdiscount and obj.userdiscount.discount:
            return obj.userdiscount.discount.name
        return 'No Discount'

    def discount_percentage(self, obj):
        if hasattr(obj, 'userdiscount') and obj.userdiscount and obj.userdiscount.discount:
            return obj.userdiscount.discount.percentage
        return ''

    has_discount.short_description = 'Discount'
    discount_percentage.short_description = 'Discount Percentage'


@admin.register(DietitianClient)
class DietitianClientAdmin(admin.ModelAdmin):
    list_display = ('dietitian_full_name', 'client_full_name', 'client_username')
    search_fields = ('dietitian__username', 'client__username')

    def dietitian_full_name(self, obj):
        return f"{obj.dietitian.first_name} {obj.dietitian.last_name}"
    dietitian_full_name.short_description = 'Dietitian'

    def client_full_name(self, obj):
        return f"{obj.client.first_name} {obj.client.last_name}"
    client_full_name.short_description = 'Client Full Name'

    def client_username(self, obj):
        return obj.client.username
    client_username.short_description = 'Client Username'


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
