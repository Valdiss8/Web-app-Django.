# Generated by Django 4.1.2 on 2023-01-19 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tisdac_app', '0019_events_visitors_marker'),
    ]

    operations = [
        migrations.AlterField(
            model_name='events',
            name='visitors_marker',
            field=models.IntegerField(blank=True, default=1),
        ),
    ]
