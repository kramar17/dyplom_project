from django.core.validators import RegexValidator
from django.db import models


class CallBackModel(models.Model):
    phone_regex = RegexValidator(regex=r'^\+?380\d{9}$|^0\d{9}$', message='Введіть ваш номер у форматі: +380xxxxxxx')
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, validators=[phone_regex])
    date = models.DateField()
    time = models.TimeField()
    comment = models.TextField(blank=True, null=True)
    is_confirmed = models.BooleanField(default=False)
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)

    def __str__(self):
        return f'{self.name} - {self.date} - {self.time}'

    class Meta:
        verbose_name = 'Заявка на дзвінок'
        verbose_name_plural = 'Заявки на дзвінок'
        ordering = ['-date_created']