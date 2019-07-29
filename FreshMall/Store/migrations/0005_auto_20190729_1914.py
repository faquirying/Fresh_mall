# Generated by Django 2.1.1 on 2019-07-29 11:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0004_goods_goods_resume'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='goods',
            name='store_id',
        ),
        migrations.AddField(
            model_name='goods',
            name='store_id',
            field=models.ForeignKey(default=5, on_delete=django.db.models.deletion.CASCADE, to='Store.Store', verbose_name='商品店铺'),
            preserve_default=False,
        ),
    ]
