# Generated by Django 2.1.1 on 2019-07-29 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Buyer', '0004_orderdetail_goods_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_id',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='id订单编号'),
        ),
    ]
