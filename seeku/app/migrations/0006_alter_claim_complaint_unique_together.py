# Generated by Django 4.2.3 on 2023-11-09 15:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_claim_complaint'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='claim_complaint',
            unique_together={('user_email', 'object_related')},
        ),
    ]
