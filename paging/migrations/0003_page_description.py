# Generated by Django 3.0.3 on 2020-03-08 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paging', '0002_auto_20200202_1900'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='description',
            field=models.CharField(blank=True, default='', max_length=1000),
        ),
    ]