# Generated by Django 5.0.6 on 2024-06-03 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_alter_dietitianclient_client_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dietitianclient',
            options={'verbose_name': 'Клієнт дієтолога', 'verbose_name_plural': 'Клієнти дієтологів'},
        ),
        migrations.AddField(
            model_name='dietitianclient',
            name='recommendation',
            field=models.TextField(blank=True, null=True),
        ),
    ]
