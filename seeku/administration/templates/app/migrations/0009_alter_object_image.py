# Generated by Django 4.2.1 on 2023-09-10 04:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_alter_object_image_alter_object_place_range'),
    ]

    operations = [
        migrations.AlterField(
            model_name='object',
            name='image',
            field=models.ImageField(upload_to='\\media'),
        ),
    ]
