# Generated by Django 2.1.7 on 2019-06-06 22:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('olsapp', '0004_auto_20190606_2232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='garage_info_table',
            name='garage_type',
            field=models.IntegerField(),
        ),
    ]
