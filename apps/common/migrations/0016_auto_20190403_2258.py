# Generated by Django 2.1.7 on 2019-04-03 22:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0015_article_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='img',
            field=models.CharField(default='', max_length=100, verbose_name='封面路径'),
        ),
    ]