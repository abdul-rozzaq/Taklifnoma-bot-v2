# Generated by Django 5.2.4 on 2025-07-13 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0009_alter_event_invitation_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.TextField(max_length=4090),
        ),
    ]
