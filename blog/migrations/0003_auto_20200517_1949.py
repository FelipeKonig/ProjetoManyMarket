# Generated by Django 3.0.6 on 2020-05-17 22:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20200517_1823'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CommonUser',
            new_name='User',
        ),
    ]
