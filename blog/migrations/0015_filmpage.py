# Generated by Django 3.2.11 on 2022-02-22 22:24

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('pelis', '0006_auto_20220209_1950'),
        ('blog', '0014_auto_20220222_2321'),
    ]

    operations = [
        migrations.CreateModel(
            name='FilmPage',
            fields=[
                ('blogpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='blog.blogpage')),
                ('titulo', models.CharField(max_length=250, verbose_name='Introducción')),
                ('cuerpo', wagtail.core.fields.RichTextField(blank=True)),
                ('pelis', modelcluster.fields.ParentalManyToManyField(blank=True, to='pelis.Pelicula')),
            ],
            options={
                'abstract': False,
            },
            bases=('blog.blogpage',),
        ),
    ]
