# Generated by Django 3.1.2 on 2020-11-11 18:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Image', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='searchquery',
            name='userWhoSearched',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='SearchQuery', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='imageurl',
            name='SearchQuery',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ImageURL', to='Image.searchquery'),
        ),
        migrations.AddField(
            model_name='image',
            name='users',
            field=models.ManyToManyField(related_name='skipped_images', to=settings.AUTH_USER_MODEL),
        ),
    ]
