# Generated by Django 2.1.7 on 2019-04-03 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0013_auto_20190403_1748'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='click_time',
            field=models.IntegerField(default=1, verbose_name='点击次数'),
        ),
    ]
