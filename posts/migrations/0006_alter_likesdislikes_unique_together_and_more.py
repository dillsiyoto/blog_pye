# Generated by Django 5.1.7 on 2025-05-07 10:53

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_likesdislikes'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='likesdislikes',
            unique_together=set(),
        ),
        migrations.AddConstraint(
            model_name='likesdislikes',
            constraint=models.UniqueConstraint(fields=('user', 'post'), name='unique_like_dislike'),
        ),
    ]
