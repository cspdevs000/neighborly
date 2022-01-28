# Generated by Django 4.0.1 on 2022-01-28 19:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('neighborly', '0007_building_creator'),
    ]

    operations = [
        migrations.AddField(
            model_name='extenduser',
            name='occupants',
            field=models.ManyToManyField(blank=True, null=True, to='neighborly.ExtendUser'),
        ),
        migrations.CreateModel(
            name='AddRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_user', to=settings.AUTH_USER_MODEL)),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
