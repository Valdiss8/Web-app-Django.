# Generated by Django 4.1.2 on 2023-01-12 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tisdac_app', '0011_alter_events_department'),
    ]

    operations = [
        migrations.AlterField(
            model_name='events',
            name='department',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
