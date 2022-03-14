# Generated by Django 3.2.5 on 2022-03-14 00:21

from django.db import migrations, models
import jsonfield.fields
import store.models.orders


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_auto_20220314_0910'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventoryhistory',
            name='type',
            field=models.CharField(choices=[('OU', 'ORDER USED'), ('RS', 'RETURN STOCK'), ('OC', 'ORDER CANCELLED'), ('BS', 'BUY STOCK')], default='OU', max_length=28),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_info',
            field=jsonfield.fields.JSONField(blank=True, default=dict, null=True),
        ),
        migrations.AlterField(
            model_name='pingoorder',
            name='delivery_info',
            field=jsonfield.fields.JSONField(blank=True, default=store.models.orders.default_delivery_info, null=True),
        ),
    ]
