# Generated by Django 4.0.6 on 2022-07-20 22:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('freemasons', '0006_freemasonmember_last_sync_at'),
    ]

    operations = [
        migrations.RenameField(
            model_name='twitteruser',
            old_name='identifier',
            new_name='inspect_identifier',
        ),
        migrations.AddField(
            model_name='twitteruser',
            name='twitter_identifier',
            field=models.CharField(max_length=256, null=True),
        ),
    ]
