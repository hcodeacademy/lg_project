# Generated by Django 4.2.4 on 2023-09-04 19:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_alter_generatedpdf_pdf_file'),
    ]

    operations = [
        migrations.RenameField(
            model_name='useraccount',
            old_name='Occupation',
            new_name='occupation',
        ),
    ]
