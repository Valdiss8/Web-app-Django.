# Generated by Django 4.1.2 on 2023-01-10 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tisdac_app', '0007_alter_events_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='events',
            name='slug',
            field=models.SlugField(default=''),
        ),
    ]
