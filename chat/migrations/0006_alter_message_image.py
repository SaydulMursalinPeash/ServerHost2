# Generated by Django 4.2.5 on 2023-09-07 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0005_message_method'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='image',
            field=models.ImageField(default=None, null=True, upload_to='message/image/'),
        ),
    ]
