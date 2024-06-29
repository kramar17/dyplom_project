"""
Admin configuration for the main app models.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import OfferModel, DiscountModel, UserDiscount, DietitianClient


@admin.register(OfferModel)
class OfferModelAdmin(admin.ModelAdmin):
    """
    Admin interface options for the OfferModel.
    """
    list_display = (
        'name', 'price', 'old_price', 'eating_plan', 'free_consultation',
        'back_up_money', 'couching', 'consultation_about_sport', 'free_week_for_family',
        'sort', 'slug'
    )
    list_editable = (
        'price', 'old_price', 'eating_plan', 'free_consultation', 'back_up_money',
        'couching', 'consultation_about_sport', 'free_week_for_family', 'sort'
    )
    prepopulated_fields = {"slug": ("name",)}


@admin.register(DiscountModel)
class DiscountAdmin(admin.ModelAdmin):
    """
    Admin interface options for the DiscountModel.
    """
    list_display = ('name', 'percentage')


class UserDiscountInline(admin.TabularInline):
    """
    Inline interface for the UserDiscount model.
    """
    model = UserDiscount
    extra = 1


class CustomUserAdmin(BaseUserAdmin):
    """
    Customized admin interface for the User model, including discount information.
    """
    inlines = (UserDiscountInline,)
    list_display = ('username', 'first_name', 'last_name', 'has_discount', 'discount_percentage', 'is_staff')

    def has_discount(self, obj: User) -> str:
        """
        Check if the user has a discount and return the discount name.
        """
        if hasattr(obj, 'userdiscount') and obj.userdiscount and obj.userdiscount.discount:
            return obj.userdiscount.discount.name
        return 'No Discount'

    def discount_percentage(self, obj: User) -> str:
        """
        Get the discount percentage for the user.
        """
        if hasattr(obj, 'userdiscount') and obj.userdiscount and obj.userdiscount.discount:
            return str(obj.userdiscount.discount.percentage)
        return ''

    has_discount.short_description = 'Discount'
    discount_percentage.short_description = 'Discount Percentage'


@admin.register(DietitianClient)
class DietitianClientAdmin(admin.ModelAdmin):
    """
    Admin interface options for the DietitianClient model.
    """
    list_display = ('dietitian_full_name', 'client_full_name', 'client_username')
    search_fields = ('dietitian__username', 'client__username')

    def dietitian_full_name(self, obj: DietitianClient) -> str:
        """
        Get the full name of the dietitian.
        """
        return f"{obj.dietitian.first_name} {obj.dietitian.last_name}"

    def client_full_name(self, obj: DietitianClient) -> str:
        """
        Get the full name of the client.
        """
        return f"{obj.client.first_name} {obj.client.last_name}"

    def client_username(self, obj: DietitianClient) -> str:
        """
        Get the username of the client.
        """
        return obj.client.username

    dietitian_full_name.short_description = 'Dietitian'
    client_full_name.short_description = 'Client Full Name'
    client_username.short_description = 'Client Username'


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
