# Generated by Django 3.0.5 on 2020-04-22 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usermanager', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermanager',
            name='name',
            field=models.CharField(default='', max_length=30),
        ),
    ]
