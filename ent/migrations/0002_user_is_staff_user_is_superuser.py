# Generated by Django 5.0.7 on 2024-08-01 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ent', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
    ]