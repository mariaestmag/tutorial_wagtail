from unicodedata import category
from django.db import models
from libros.models import Libro
from django import forms
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel,  MultiFieldPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet
from wagtail.search import index
from wagtailgeowidget.edit_handlers import LeafletPanel

from pelis.models import Pelicula


class BlogIndexPage(Page):
    # Sólo puede haber un index
    max_count = 1

    # Parent page / subpage type rules
    parent_page_types = ['home.HomePage']
    subpage_types = ['blog.BlogPage','blog.FilmPage','blog.TravelPage','blog.BookPage']

    introduccion = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('introduccion', classname="full")
    ]

    def get_context(self, request):
        # Lista de blogs empezando por el más antiguo 
        context = super().get_context(request)
        blogpages = self.get_children().live().order_by('-first_published_at')
        context['blogpages'] = blogpages
        return context

class BlogTagIndexPage(Page):
    # Sólo puede haber un index
    max_count = 1

    def get_context(self, request):
        # Filtra por tag cuando lo pida la página
        tag = request.GET.get('tag')
        blogpages = BlogPage.objects.filter(tags__name=tag)
        context = super().get_context(request)
        context['blogpages'] = blogpages
        return context

@register_snippet
class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'BlogPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'


class BlogPage(Page):
    # Campos para cuando queramos crear una página blog genérica
    date = models.DateField("Fecha Post")
    intro = models.CharField("Introducción", max_length=250)
    body = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    categories = ParentalManyToManyField('blog.BlogCategory', blank=True)

    # Parent page / subpage type rules
    parent_page_types = ['blog.BlogIndexPage']
    subpage_types = []

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('tags'),
            FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
            ],
            heading='Información'
        ),
        FieldPanel('intro'),
        FieldPanel('body', classname="full"),
        InlinePanel('gallery_images', 
            label="Galería de imágenes"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        blogpages = BlogPage.objects.all()
        categoria_id = request.GET.get('categoria')

        if categoria_id:
            blogpages = BlogPage.objects.filter(blogcategory__id=categoria_id) #sobreescribo la lista de libros con la condición

        context['blogpages'] = blogpages 
      
        return context    


class FilmPage(BlogPage):

    # Parent page / subpage type rules
    parent_page_types = ['blog.BlogIndexPage']
    subpage_types = []


    # Al heredar de BlogPage, hereda sus atributos
    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'), 
    ]

    # Pasamos campos de BlogPage para el CMS así como el atributo creado para este tipo de páginas
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('intro'),
            FieldPanel('body'),
            FieldPanel('tags'),
            FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
            FieldPanel('date'),
            InlinePanel('lista_pelis')
            ],
            heading='Información'
        ),
    ] 

class PeliculasOrderable(Orderable):
    #Permite seleccionar pelicula desde Snippets (Fragmentos)
    page = ParentalKey(FilmPage, 
        on_delete=models.CASCADE, 
        related_name='lista_pelis')
    
    pelicula = models.ForeignKey(
        "pelis.Pelicula",
        on_delete=models.CASCADE, related_name="+"
    )

    panels = [
    	# Usamos SnippetChooserPanel porque peli.Pelicula está registrada como tal
        SnippetChooserPanel("pelicula"),
    ]

class TravelPage(BlogPage):

     # Parent page / subpage type rules
    parent_page_types = ['blog.BlogIndexPage']
    subpage_types = []

    # Campos para cuando queramos crear una página sobre viajes, hereda campos de BlogPage
    location = models.CharField(max_length=250, blank=True, null=True)  

    # Pasamos campos de BlogPage para su búsqueda
    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    # Pasamos campos de BlogPage para el CMS así como el atributo creado para este tipo de páginas
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('intro'),
            FieldPanel('body'),
            FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
            FieldPanel('date'),
            LeafletPanel('location'),
            ],
            heading='Información'
        ),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        locations = TravelPage.objects.filter(blogpage_ptr_id=15) #busco la tupla que contiene los datos
        text = locations.first().location
        coordenadas = text[text.rindex("(")+1 : text.rindex(")")].split()
        context['longitud'] = coordenadas[0]
        context['latitud'] = coordenadas[1]
        return context


class BookPage(BlogPage):
    
    # Parent page / subpage type rules
    parent_page_types = ['blog.BlogIndexPage']
    subpage_types = []


    # Pasamos campos de BlogPage para su búsqueda
    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    # Pasamos campos de BlogPage para el CMS así como el atributo creado para este tipo de páginas
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('intro'),
            FieldPanel('body'),
            FieldPanel('tags'),
            FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
            FieldPanel('date'),
            InlinePanel('lista_libros')
            ],
            heading='Información'
        ),
    ]

    def get_context(self, request):
        libros = Libro.objects.all()
        context = super().get_context(request)
        context['libros'] = libros
        return context

class LibrosOrderable(Orderable):
    #Permite seleccionar libro desde Snippets (Fragmentos)
    page = ParentalKey(BookPage, 
        on_delete=models.CASCADE, 
        related_name='lista_libros')
    
    libro = models.ForeignKey(
        "libros.Libro",
        on_delete=models.CASCADE, related_name="+"
    )

    panels = [
    	# Usamos SnippetChooserPanel porque libros.Libro está registrada como tal
        SnippetChooserPanel("libro"),
    ]


class BlogPageGalleryImage(Orderable):
    page = ParentalKey(BlogPage, 
        on_delete=models.CASCADE, 
        related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]


class BlogCategoryIndexPage(Page):
    # Sólo puede haber un index
    max_count = 1

    def get_context(self, request):
        # Filtra por tag cuando lo pida la página
        categoria = request.GET.get('categoria')
        blogpages = BlogPage.objects.filter(categories=categoria)
        context = super().get_context(request)
        context['blogpages'] = blogpages
        return context

@register_snippet
class BlogCategory(models.Model):
    # Crea categorías
    name = models.CharField(max_length=255)
    icon = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )

    panels = [
        FieldPanel('name'),
        ImageChooserPanel('icon'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categorías de blog'
        verbose_name = 'categoría de blog'


@register_snippet
class FooterText(models.Model):
    # Crea vínculos para el footer
    body = models.CharField(max_length=255)
    url = models.URLField(null=True)

    panels = [
        FieldPanel('body'),
        FieldPanel('url'),
    ]

    def __str__(self):
        return self.body

    class Meta:
        verbose_name_plural = 'Footer Text'