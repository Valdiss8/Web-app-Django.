# Generated by Django 4.1.2 on 2023-01-19 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tisdac_app', '0023_alter_news_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='events',
            name='visitors',
            field=models.ManyToManyField(blank=True, to='tisdac_app.visitor'),
        ),
    ]
