from django.contrib.auth.models import User
from django.db import models


class OfferModel(models.Model):
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
        return self.name

    class Meta:
        verbose_name_plural = 'Наші пропозиції'
        verbose_name = 'Пропозиція'
        ordering = ['sort']


class DiscountModel(models.Model):
    name = models.CharField(max_length=255)
    percentage = models.FloatField()

    def __str__(self):
        return f"{self.name} ({self.percentage}%)"


class UserDiscount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    discount = models.ForeignKey(DiscountModel, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.discount.name if self.discount else 'Немає Знижки'}"


class DietitianClient(models.Model):
    dietitian = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='Дієтологи',
        limit_choices_to={'is_staff': True}
    )
    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='Клієнти',
        limit_choices_to={'is_staff': False}
    )

    def __str__(self):
        return f'{self.dietitian.username} - {self.client.username}'

    class Meta:
        verbose_name = "Клієнт дієтолога"
        verbose_name_plural = "Клієнти дієтологів"




