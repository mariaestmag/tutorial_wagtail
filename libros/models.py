from django.db import models
from wagtail.core.models import Page 
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel

from django.utils.text import slugify

class Libro(models.Model):
    title = models.CharField('título', max_length=250)
    author = models.CharField('autor', max_length=250)
    summary = models.CharField('sinopsis', max_length=500)
    slug = models.SlugField(blank=True)
    imagen = models.URLField()

    panels = [
        FieldPanel('title'),
        FieldPanel('slug'),
        FieldPanel('author'),
        FieldPanel('summary'),
        FieldPanel('imagen')
    ]
    def __str__(self):
        return f'{self.title} ({self.author})'
    
    class Meta:
        verbose_name = 'Libro'
        verbose_name_plural = 'Libros'
        
class LibrosIndexPage(Page):
    max_count = 1

    introduccion = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('introduccion', classname="full")
    ]
