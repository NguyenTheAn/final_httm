# Generated by Django 3.0.5 on 2021-06-14 09:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0002_auto_20210614_1402'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='historylineid',
        ),
        migrations.AddField(
            model_name='historyline',
            name='orderid',
            field=models.ForeignKey(db_column='OrderID', default=None, on_delete=django.db.models.deletion.CASCADE, to='ecomapp.Order'),
            preserve_default=False,
        ),
    ]
