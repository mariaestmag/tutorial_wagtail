from pydoc import classname
from re import template
from turtle import title
from django.db import models
from wagtail.core.models import Page 
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.text import slugify
from wagtail.search import index
from wagtail.snippets.models import register_snippet


@register_snippet
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


class LibroDetailPage(Page):
    max_count = 1

    introduccion = RichTextField(blank=True)
    body = RichTextField(blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('introduccion'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('introduccion', classname="full"),
        FieldPanel('body', classname="full"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        libros = Libro.objects.all()
        libro_id = request.GET.get('libro')

        if libro_id:
            libros = Libro.objects.filter(id=libro_id) #sobreescribo la lista de libros con la condición

        context['libros'] = libros 
      
        return context
        
class LibrosIndexPage(Page):
    max_count = 1

    introduccion = RichTextField(blank=True)

    subpage_types = ['libros.LibroDetailPage',]

    content_panels = Page.content_panels + [
        FieldPanel('introduccion', classname="full")
    ]

    def paginate(self, request, libros, *args):
        page = request.GET.get('page')
        
        paginator = Paginator(libros, 15)
        try:
            pages = paginator.page(page)
        except PageNotAnInteger:
            pages = paginator.page(1)
        except EmptyPage:
            pages = paginator.page(paginator.num_pages)
        return pages

    def get_context(self, request):
        context = super().get_context(request)
        libros = Libro.objects.all()
        context['libros'] = self.paginate(request, libros)        
        return context
