# Generated by Django 3.1.2 on 2020-11-10 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Quotes',
            fields=[
                ('quotesID', models.CharField(max_length=16, primary_key=True, serialize=False)),
                ('quote', models.CharField(max_length=300)),
            ],
        ),
    ]
