# Generated by Django 2.2.3 on 2019-07-11 09:03

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=120)),
                ('description', models.CharField(blank=True, max_length=200)),
                ('label', models.CharField(blank=True, max_length=150)),
                ('is_archive', models.BooleanField(blank=True, default=False)),
                ('is_trash', models.BooleanField(blank=True, default=False)),
                ('is_pin', models.BooleanField(blank=True, default=False)),
                ('color', models.CharField(blank=True, max_length=100)),
                ('images', models.ImageField(blank=True, upload_to='images/%Y/%m/%d')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Userprofile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, validators=[django.core.validators.RegexValidator('^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')])),
                ('email', models.EmailField(max_length=200)),
                ('password', models.CharField(blank=True, max_length=100)),
                ('username', models.CharField(blank=True, max_length=100)),
            ],
        ),
    ]
