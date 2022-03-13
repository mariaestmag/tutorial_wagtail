from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel,  MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet
from wagtail.search import index


class NewsIndexPage(Page):
    max_count = 1

    # Parent page / subpage type rules
    parent_page_types = ['home.HomePage']
    subpage_types = ['noticias.NewsPage']

    introduccion = RichTextField(blank=True)

    # Éste index sólo puede permitir los siguientes tipos de páginas
    subpage_types = ['noticias.NewsPage']

    content_panels = Page.content_panels + [
        FieldPanel('introduccion', classname="full")
    ]

    def get_context(self, request):
        # Devuelve lista de los subtipos anteriores mientras estén públicos y ordenados por fecha siendo el más antiguo el primero 
        context = super().get_context(request)
        noticias = self.get_children().live().order_by('-first_published_at')[:5]
        context['noticias'] = noticias
        return context

@register_snippet
class NewsPage(Page):
    date = models.DateField("Fecha Post", blank=True)
    intro = models.CharField("Introducción", max_length=250)
    summary = RichTextField(blank=True)
    body = RichTextField(blank=True)

    # Parent page / subpage type rules
    parent_page_types = ['noticias.NewsIndexPage']
    subpage_types = []

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
        index.SearchField('summary'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date')
            ],
            heading='Información'
        ),
        FieldPanel('intro'),
        FieldPanel('body', classname="full"),
        FieldPanel('summary', classname="full"),
        InlinePanel('gallery_images', label="Galería de imágenes"),
    ]

    def noticias(self, request):
        context = super().get_context(request)
        noticias = self.get_children().live().order_by('-date')[:5]
        context['news'] = noticias
        return context
        
class NewsPageGalleryImage(Orderable):
    page = ParentalKey(NewsPage, 
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

    