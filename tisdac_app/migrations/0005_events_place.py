# Generated by Django 4.1.2 on 2023-01-10 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tisdac_app', '0004_events_repeatable_alter_events_department'),
    ]

    operations = [
        migrations.AddField(
            model_name='events',
            name='place',
            field=models.CharField(default='Mere pst. 3', max_length=200),
        ),
    ]
