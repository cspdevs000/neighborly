# Generated by Django 4.0.1 on 2022-01-25 21:00

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('neighborly', '0002_extenduser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='pub_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='reply',
            name='pub_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]