# Generated by Django 3.1.7 on 2021-03-10 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resume', '0004_resumefile_uuidcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resumefile',
            name='uuidcode',
            field=models.CharField(max_length=40),
        ),
    ]
