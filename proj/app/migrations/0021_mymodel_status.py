# Generated by Django 5.1.4 on 2025-01-29 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_alter_customuser_type_of_worker'),
    ]

    operations = [
        migrations.AddField(
            model_name='mymodel',
            name='status',
            field=models.CharField(default='process', max_length=30),
        ),
    ]
