# Generated by Django 5.1.6 on 2025-02-07 04:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
    ]
