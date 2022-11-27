# Generated by Django 4.1.3 on 2022-11-20 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_order_place'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='place',
        ),
        migrations.AddField(
            model_name='restaurant',
            name='items',
            field=models.ManyToManyField(to='base.item'),
        ),
    ]
