# Generated by Django 4.1.2 on 2022-11-03 09:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='update_at',
            new_name='updated_at',
        ),
        migrations.RenameField(
            model_name='room',
            old_name='update_at',
            new_name='updated_at',
        ),
    ]
