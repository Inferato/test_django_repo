# Generated by Django 5.1.6 on 2025-03-13 17:45

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAdress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=100, verbose_name='Місто')),
                ('street', models.CharField(max_length=150, verbose_name='Вулиця')),
                ('postal_code', models.CharField(max_length=10, verbose_name='Індекс')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='adresses', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Адреса користувача',
                'verbose_name_plural': 'Адреси користувачів',
            },
        ),
        migrations.CreateModel(
            name='UserPaymant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Сума')),
                ('payment_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата платежу')),
                ('payment_method', models.CharField(choices=[('card', 'Карта'), ('cash', 'Готівка'), ('iban', 'Рахунок')], default='card', max_length=50, verbose_name='Метод оплати')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
