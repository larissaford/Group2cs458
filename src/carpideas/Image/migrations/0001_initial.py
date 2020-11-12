
# Generated by Django 3.1.2 on 2020-11-10 17:01

from django.db import migrations, models
import django.db.models.deletion



class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(

            name='SearchQuery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userSearchQuery', models.CharField(max_length=255, unique=True)),
                ('lastSearched', models.DateTimeField(auto_now_add=True)),

            ],
        ),
        migrations.CreateModel(
            name='ImageURL',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=255, unique=True)),

                ('imageSeenOn', models.DateTimeField(auto_now_add=True)),
                ('imageLiked', models.BooleanField()),
                ('imageDisliked', models.BooleanField()),
                ('searchQuery', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ImageURL', to='Image.searchquery')),

            ],
        ),
    ]
