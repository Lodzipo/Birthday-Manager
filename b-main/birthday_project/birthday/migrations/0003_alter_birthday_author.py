# Generated by Django 3.2.16 on 2024-12-07 12:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('birthday', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='birthday',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.myuser', verbose_name='Автор записи'),
        ),
    ]
