# Generated by Django 3.1.1 on 2020-09-07 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('soldiers_viewer', '0003_auto_20200907_2011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='soldier',
            name='regiment',
            field=models.CharField(max_length=100),
        ),
    ]
