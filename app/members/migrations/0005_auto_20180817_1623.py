# Generated by Django 2.1 on 2018-08-17 07:23

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0004_auto_20180817_1622'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='funding',
            field=models.ManyToManyField(blank=True, related_name='funding_list', related_query_name='funding_list', through='members.Funding', to=settings.AUTH_USER_MODEL),
        ),
    ]
