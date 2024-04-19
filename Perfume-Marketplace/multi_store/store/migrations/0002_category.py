# Generated by Django 4.1.3 on 2023-06-25 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('type1', models.IntegerField(choices=[(1, 'Woody'), (2, 'Floral'), (3, 'Oriental'), (4, 'Fresh'), (5, 'Celebrity Scents')], null=True)),
                ('type2', models.IntegerField(choices=[(1, 'Fresh Floral'), (2, 'Fruity Floral'), (3, 'Oriental Floral'), (4, 'Classic Oriental'), (5, 'Woody Oriental'), (6, 'Fresh Water'), (7, 'Fresh Citrus'), (8, 'Fresh Green'), (9, 'Woody Mossy'), (10, 'Woody Smokey'), (11, 'Celebrity Scents'), (12, 'Fresh Oriental')], null=True)),
            ],
        ),
    ]
