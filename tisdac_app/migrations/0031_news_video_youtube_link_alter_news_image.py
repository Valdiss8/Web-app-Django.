# Generated by Django 4.1.2 on 2023-01-23 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tisdac_app', '0030_alter_department_image2'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='video_youtube_link',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='news',
            name='image',
            field=models.FileField(null=True, upload_to='news'),
        ),
    ]
