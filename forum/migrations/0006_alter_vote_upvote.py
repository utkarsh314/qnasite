# Generated by Django 4.0 on 2022-01-29 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0005_vote'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vote',
            name='upvote',
            field=models.BooleanField(),
        ),
    ]
