# Generated by Django 2.2.5 on 2021-06-18 23:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='proweb_file',
            old_name='type',
            new_name='types',
        ),
    ]
