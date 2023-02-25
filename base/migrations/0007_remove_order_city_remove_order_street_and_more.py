# Generated by Django 4.1.6 on 2023-02-25 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_order_completed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='city',
        ),
        migrations.RemoveField(
            model_name='order',
            name='street',
        ),
        migrations.AlterField(
            model_name='order',
            name='combined_price',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='completed',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery_price',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]