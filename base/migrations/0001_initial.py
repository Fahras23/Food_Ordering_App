# Generated by Django 4.1.6 on 2023-02-13 16:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('type', models.CharField(choices=[('food', 'food'), ('drink', 'drink')], default='food', max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='RestaurantLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street', models.CharField(blank=True, max_length=30)),
                ('city', models.CharField(blank=True, max_length=30)),
                ('country', models.CharField(blank=True, max_length=30)),
                ('postcode', models.CharField(blank=True, max_length=30)),
                ('xmap', models.DecimalField(decimal_places=4, max_digits=10)),
                ('ymap', models.DecimalField(decimal_places=4, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(max_length=100)),
                ('addition_date', models.DateTimeField(auto_now_add=True)),
                ('type', models.CharField(choices=[('Asian', 'Asian'), ('Italian', 'Italian'), ('Gregorian', 'Gregorian'), ('American', 'American'), ('Polish', 'Polish')], default='default', max_length=32)),
                ('value', models.CharField(choices=[('$', 1), ('$$', 2), ('$$$', 3)], default='default', max_length=32)),
                ('location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.restaurantlocation')),
            ],
            options={
                'ordering': ['-addition_date'],
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quanity_for_order', models.DecimalField(decimal_places=0, max_digits=2)),
                ('items', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.item')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('combined_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('delivery_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('street', models.TextField(max_length=100)),
                ('city', models.TextField(max_length=100)),
                ('items', models.ManyToManyField(to='base.orderitem')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='place',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.restaurant'),
        ),
    ]
