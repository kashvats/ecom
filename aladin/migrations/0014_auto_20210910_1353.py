# Generated by Django 2.2.14 on 2021-09-10 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aladin', '0013_auto_20210909_1249'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='itemss',
        ),
        migrations.AddField(
            model_name='order',
            name='itemss',
            field=models.TextField(blank=True),
        ),
    ]
