# Generated by Django 4.0 on 2023-07-16 00:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_alter_useraccount_gender_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='marital_status',
            field=models.IntegerField(choices=[(0, 'Single'), (1, 'Married'), (2, 'Divorced')]),
        ),
        migrations.AlterField(
            model_name='useraccount',
            name='passport',
            field=models.ImageField(upload_to=''),
        ),
    ]
