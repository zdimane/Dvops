# Generated by Django 4.1.3 on 2023-06-25 17:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_alter_order_date_rate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateField(default=datetime.datetime(2023, 6, 25, 17, 36, 43, 265880, tzinfo=datetime.timezone.utc)),
        ),
    ]
