from django.contrib.auth.models import User
from django.db import models


class OfferModel(models.Model):
    """
    Model representing an offer.

    Attributes:
        name (str): The name of the offer.
        price (int): The price of the offer.
        old_price (int): The old price of the offer.
        eating_plan (bool): Whether the offer includes an eating plan.
        free_consultation (bool): Whether the offer includes a free consultation.
        back_up_money (bool): Whether the offer includes a money-back guarantee.
        couching (bool): Whether the offer includes coaching.
        consultation_about_sport (bool): Whether the offer includes sports consultation.
        free_week_for_family (bool): Whether the offer includes a free week for family.
        sort (int): Sorting order of the offer.
        slug (str): Slug field for URL representation.
        is_visible (bool): Whether the offer is visible on the website.
    """

    name = models.CharField(max_length=100)
    price = models.IntegerField()
    old_price = models.IntegerField()
    eating_plan = models.BooleanField()
    free_consultation = models.BooleanField()
    back_up_money = models.BooleanField()
    couching = models.BooleanField()
    consultation_about_sport = models.BooleanField()
    free_week_for_family = models.BooleanField()
    sort = models.PositiveSmallIntegerField()
    slug = models.SlugField(max_length=255)
    is_visible = models.BooleanField()

    def __str__(self):
        """
        String representation of the offer object.

        Returns:
            str: Name of the offer.
        """
        return self.name

    class Meta:
        verbose_name_plural = 'Наші пропозиції'
        verbose_name = 'Пропозиція'
        ordering = ['sort']


class DiscountModel(models.Model):
    """
    Model representing a discount.

    Attributes:
        name (str): The name of the discount.
        percentage (float): The percentage value of the discount.
    """

    name = models.CharField(max_length=255)
    percentage = models.FloatField()

    def __str__(self):
        """
        String representation of the discount object.

        Returns:
            str: Name and percentage of the discount.
        """
        return f"{self.name} ({self.percentage}%)"


class UserDiscount(models.Model):
    """
    Model representing a user's discount.

    Attributes:
        user (User): The user associated with the discount.
        discount (DiscountModel): The discount applied to the user.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    discount = models.ForeignKey(DiscountModel, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        """
        String representation of the user discount object.

        Returns:
            str: Username and discount name (if available).
        """
        return f"{self.user.username} - {self.discount.name if self.discount else 'Немає Знижки'}"


class DietitianClient(models.Model):
    """
    Model representing a relationship between a dietitian and a client.

    Attributes:
        dietitian (User): The dietitian associated with the client.
        client (User): The client associated with the dietitian.
        recommendation (str): Recommendation or notes related to the client (optional).
    """

    dietitian = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='dietitians',
        limit_choices_to={'is_staff': True}
    )
    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='clients',
        limit_choices_to={'is_staff': False}
    )

    recommendation = models.TextField(blank=True, null=True)

    def __str__(self):
        """
        String representation of the DietitianClient object.

        Returns:
            str: Username of the dietitian and client.
        """
        return f'{self.dietitian.username} - {self.client.username}'

    class Meta:
        verbose_name = "Клієнт дієтолога"
        verbose_name_plural = "Клієнти дієтологів"
