# Generated by Django 3.0.5 on 2020-04-26 23:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_main_aboutdetail'),
    ]

    operations = [
        migrations.AddField(
            model_name='main',
            name='activate',
            field=models.CharField(default=0, max_length=30),
        ),
    ]