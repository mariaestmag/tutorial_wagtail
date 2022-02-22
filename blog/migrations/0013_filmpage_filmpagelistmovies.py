# Generated by Django 3.2.11 on 2022-02-22 09:47

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_auto_20220216_1044'),
    ]

    operations = [
        migrations.CreateModel(
            name='FilmPage',
            fields=[
                ('blogpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='blog.blogpage')),
                ('titulo', models.CharField(max_length=250, verbose_name='Introducción')),
                ('desarrollo', wagtail.core.fields.RichTextField(blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('blog.blogpage',),
        ),
        migrations.CreateModel(
            name='FilmPageListMovies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('descripcion', models.CharField(blank=True, max_length=250)),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='list_movies', to='blog.filmpage')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
    ]
