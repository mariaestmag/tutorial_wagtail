# Generated by Django 3.2.11 on 2022-02-24 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0016_musicpage_travelpage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='travelpage',
            name='cuerpo',
        ),
        migrations.RemoveField(
            model_name='travelpage',
            name='titulo',
        ),
        migrations.AddField(
            model_name='travelpage',
            name='location',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
