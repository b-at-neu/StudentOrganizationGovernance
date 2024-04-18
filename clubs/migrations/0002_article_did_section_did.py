# Generated by Django 5.0.2 on 2024-04-17 11:19

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='did',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
        migrations.AddField(
            model_name='section',
            name='did',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]