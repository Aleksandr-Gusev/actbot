# Generated by Django 5.1.4 on 2025-01-21 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_mymodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mymodel',
            name='number_act',
            field=models.IntegerField(),
        ),
    ]
