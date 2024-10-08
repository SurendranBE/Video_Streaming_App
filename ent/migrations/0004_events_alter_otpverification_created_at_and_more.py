# Generated by Django 5.0.7 on 2024-08-02 09:51

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ent', '0003_otpverification'),
    ]

    operations = [
        migrations.CreateModel(
            name='Events',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
            ],
        ),
        migrations.AlterField(
            model_name='otpverification',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='otpverification',
            name='otp',
            field=models.CharField(max_length=6),
        ),
        migrations.AlterField(
            model_name='otpverification',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Subtitle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subtitle', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('video_link', models.URLField()),
                ('image', models.ImageField(upload_to='subtitles/images/')),
                ('content', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subtitles', to='ent.events')),
            ],
        ),
    ]
