# Generated by Django 2.0.7 on 2018-08-07 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reward', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_description',
            field=models.TextField(blank=True),
        ),
    ]