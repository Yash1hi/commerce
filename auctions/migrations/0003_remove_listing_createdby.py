# Generated by Django 3.0.8 on 2020-07-31 00:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_bid_comment_listing'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='createdBy',
        ),
    ]
