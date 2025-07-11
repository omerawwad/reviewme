# Generated by Django 5.1.7 on 2025-05-14 19:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviewme', '0004_review_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnswerLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='reviewme.answer')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answer_likes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Answer Like',
                'verbose_name_plural': 'Answer Likes',
                'unique_together': {('user', 'answer')},
            },
        ),
        migrations.CreateModel(
            name='QuestionUpvote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='upvotes', to='reviewme.question')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_upvotes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Question Upvote',
                'verbose_name_plural': 'Question Upvotes',
                'unique_together': {('user', 'question')},
            },
        ),
        migrations.CreateModel(
            name='ReviewLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='reviewme.review')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review_likes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Review Like',
                'verbose_name_plural': 'Review Likes',
                'unique_together': {('user', 'review')},
            },
        ),
    ]
