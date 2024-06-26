# Generated by Django 5.0.2 on 2024-03-08 09:10

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Club',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(default=None, max_length=200, unique=True)),
                ('url', models.CharField(default=None, max_length=50, unique=True)),
                ('abbreviation', models.CharField(default=None, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Constitution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('submitted_timestamp', models.DateTimeField(default=None, null=True)),
                ('reviewed_timestamp', models.DateTimeField(default=None, null=True)),
                ('status', models.IntegerField(choices=[(1, 'Approved'), (2, 'Denied'), (3, 'Conditionally Approved'), (4, 'Edited'), (5, 'Submitted')], default=None)),
                ('club', models.ForeignKey(default=None, editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='constitutions', to='clubs.club')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveSmallIntegerField(default=None, validators=[django.core.validators.MinValueValidator(1)])),
                ('title', models.CharField(default=None, max_length=200)),
                ('constitution', models.ForeignKey(default=None, editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='articles', to='clubs.constitution')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveSmallIntegerField(default=None, validators=[django.core.validators.MinValueValidator(1)])),
                ('content', models.CharField(default=None, max_length=10000)),
                ('article', models.ForeignKey(default=None, editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='sections', to='clubs.article')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
