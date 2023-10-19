# Generated by Django 4.2.1 on 2023-10-14 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='object',
            name='object_recovered',
            field=models.CharField(choices=[('Recovered', 'Recovered'), ('Not Recovered', 'Not Recovered')], default='Not Recovered', max_length=100),
        ),
        migrations.AddField(
            model_name='object',
            name='object_status',
            field=models.CharField(choices=[('Claimed', 'Claimed'), ('Not Claimed', 'Not Claimed')], default='Not Claimed', max_length=100),
        ),
        migrations.AddField(
            model_name='object',
            name='place_registered',
            field=models.CharField(choices=[('Library', 'Library'), ('Block 3', 'Block 3')], default='Block 3', max_length=100),
        ),
    ]
