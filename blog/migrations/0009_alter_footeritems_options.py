# Generated by Django 3.2.11 on 2022-02-12 20:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_footeritems'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='footeritems',
            options={'verbose_name': 'Item', 'verbose_name_plural': 'Footer items'},
        ),
    ]
