# Generated by Django 4.2.3 on 2023-11-09 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_alter_claim_complaint_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='object',
            name='user_claimer',
            field=models.EmailField(blank=True, max_length=254),
        ),
    ]