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

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Наші пропозиції'
        verbose_name = 'Пропозиція'
        ordering = ['sort']
