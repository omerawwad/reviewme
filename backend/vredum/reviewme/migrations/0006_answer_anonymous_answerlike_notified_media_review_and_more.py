# Generated by Django 5.1.7 on 2025-05-30 03:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviewme', '0005_answerlike_questionupvote_reviewlike'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='anonymous',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='answerlike',
            name='notified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='media',
            name='review',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='links', to='reviewme.review'),
        ),
        migrations.AddField(
            model_name='question',
            name='anonymous',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='questionupvote',
            name='notified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='review',
            name='anonymous',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='reviewlike',
            name='notified',
            field=models.BooleanField(default=False),
        ),
    ]
