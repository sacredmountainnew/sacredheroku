# Generated by Django 3.0.5 on 2020-04-29 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usermanager', '0003_usermanager_ip'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermanager',
            name='geolocation',
            field=models.TextField(default=''),
        ),
    ]