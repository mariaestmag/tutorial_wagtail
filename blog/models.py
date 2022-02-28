from ctypes.wintypes import POINT
from django.db import models
from libros.models import Libro
from django import forms
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel,  MultiFieldPanel, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet
from wagtail.search import index
from wagtailgeowidget.edit_handlers import LeafletPanel
from djgeojson.fields import PointField



class BlogIndexPage(Page):
    max_count = 1

    subpage_types = ['blog.BlogPage','blog.FilmPage','blog.TravelPage','blog.BookPage']

    introduccion = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('introduccion', classname="full")
    ]

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        blogpages = self.get_children().live().order_by('-first_published_at')
        context['blogpages'] = blogpages
        
        return context

class BlogTagIndexPage(Page):
    max_count = 1

    def get_context(self, request):

        # Filter by tag
        tag = request.GET.get('tag')
        blogpages = BlogPage.objects.filter(tags__name=tag)

        # Update template context
        context = super().get_context(request)
        context['blogpages'] = blogpages
        return context

class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'BlogPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


class BlogPage(Page):
    date = models.DateField("Fecha Post")
    intro = models.CharField("Introducción", max_length=250)
    body = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    categories = ParentalManyToManyField('blog.BlogCategory', blank=True)


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

class FilmPage(BlogPage):
    titulo = models.CharField("Introducción", max_length=250)
    cuerpo = RichTextField(blank=True)
    pelis = ParentalManyToManyField('pelis.Pelicula', blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('titulo'),
        index.SearchField('cuerpo'), 
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('titulo'),
            FieldPanel('cuerpo'),
            FieldPanel('pelis', widget=forms.Select),
            ],
            heading='Información'
        ),
    ] 
  
class TravelPage(BlogPage):
    
    location = models.CharField(max_length=250, blank=True, null=True)  

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('intro'),
            FieldPanel('body'),
            FieldPanel('date'),
            LeafletPanel('location'),
            ],
            heading='Información'
        ),
    ]

class BookPage(BlogPage):

    libros = ParentalManyToManyField('libros.Libro', blank=True)


    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('intro'),
            FieldPanel('body'),
            FieldPanel('date'),
            #FieldPanel('libros', widget=forms.Select),
            ],
            heading='Información'
        ),
    ]

    def get_context(self, request):
        libros = Libro.objects.all()
        context = super().get_context(request)
        context['libros'] = libros
        return context

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

@register_snippet
class BlogCategory(models.Model):
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
    """
    This provides editable text for the site footer. Again it uses the decorator
    `register_snippet` to allow it to be accessible via the admin. It is made
    accessible on the template via a template tag defined in base/templatetags/
    navigation_tags.py
    """
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