# Generated by Django 4.1.3 on 2022-11-20 16:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_remove_item_place_restaurant_items'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='place',
        ),
        migrations.RemoveField(
            model_name='restaurant',
            name='items',
        ),
        migrations.AddField(
            model_name='item',
            name='place',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.restaurant'),
        ),
    ]