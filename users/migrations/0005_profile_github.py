# Generated by Django 3.2.7 on 2021-09-12 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_profile_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='github',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
