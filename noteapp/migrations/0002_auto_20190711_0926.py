# Generated by Django 2.2.3 on 2019-07-11 09:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('noteapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='note',
            old_name='created',
            new_name='created_by',
        ),
    ]
