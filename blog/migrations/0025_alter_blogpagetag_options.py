# Generated by Django 3.2.11 on 2022-03-06 12:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0024_auto_20220301_1249'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blogpagetag',
            options={'verbose_name': 'Tag', 'verbose_name_plural': 'Tags'},
        ),
    ]
