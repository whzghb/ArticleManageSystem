# Generated by Django 2.1.7 on 2019-03-30 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0008_log_add_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='name',
            field=models.CharField(default='', max_length=100, verbose_name='名称'),
        ),
    ]
