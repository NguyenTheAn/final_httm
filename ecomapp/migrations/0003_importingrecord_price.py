# Generated by Django 3.2.4 on 2021-06-18 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0002_importingrecord_num'),
    ]

    operations = [
        migrations.AddField(
            model_name='importingrecord',
            name='price',
            field=models.IntegerField(blank=True, db_column='Price', null=True),
        ),
    ]