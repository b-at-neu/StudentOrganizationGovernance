# Generated by Django 5.0.2 on 2024-04-17 11:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0002_article_did_section_did'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='article',
            unique_together={('constitution', 'did')},
        ),
        migrations.AlterUniqueTogether(
            name='section',
            unique_together={('article', 'did')},
        ),
    ]