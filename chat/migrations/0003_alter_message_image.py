# Generated by Django 4.2.3 on 2023-08-02 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_message_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='image',
            field=models.TextField(blank=True, default=None, max_length=3000, null=True),
        ),
    ]
