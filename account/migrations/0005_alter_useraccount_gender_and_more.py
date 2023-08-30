# Generated by Django 4.2.3 on 2023-07-15 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_alter_useraccount_gender_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='gender',
            field=models.IntegerField(choices=[(0, 'Male'), (1, 'Female')]),
        ),
        migrations.AlterField(
            model_name='useraccount',
            name='marital_status',
            field=models.IntegerField(choices=[(0, 'Single'), (1, 'Married'), (2, 'Divored')]),
        ),
    ]