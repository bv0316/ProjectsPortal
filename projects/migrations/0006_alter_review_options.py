# Generated by Django 3.2.7 on 2021-09-18 21:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_rename_users_project_owner'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ['-created']},
        ),
    ]
