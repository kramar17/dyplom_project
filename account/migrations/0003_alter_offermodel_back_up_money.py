# Generated by Django 5.0.6 on 2024-06-01 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_offermodel_eating_plan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offermodel',
            name='back_up_money',
            field=models.BooleanField(),
        ),
    ]
