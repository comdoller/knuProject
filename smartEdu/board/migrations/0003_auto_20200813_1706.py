# Generated by Django 3.0.8 on 2020-08-13 08:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0002_auto_20200813_1705'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='c_wirter',
            new_name='c_writer',
        ),
    ]