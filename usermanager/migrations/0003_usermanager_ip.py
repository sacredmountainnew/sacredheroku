# Generated by Django 3.0.5 on 2020-04-29 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usermanager', '0002_usermanager_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermanager',
            name='ip',
            field=models.TextField(default=''),
        ),
    ]