# Generated by Django 5.1.3 on 2024-11-30 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='avatar',
            field=models.ImageField(null=True, upload_to='groups/'),
        ),
    ]