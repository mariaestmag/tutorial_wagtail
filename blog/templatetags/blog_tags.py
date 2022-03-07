from blog.models import BlogCategory as Category, BlogPageTag
from blog.models import FooterText
from noticias.models import NewsPage
from django.template import Library, loader
from django import template


register = template.Library()


@register.inclusion_tag('blog/components/categories_list.html',
                        takes_context=True)
def categories_list(context):
    categories = Category.objects.all()
    return {
        'request': context['request'],
        'categories': categories
    }

@register.inclusion_tag('blog/components/footer_text.html', takes_context=True)
def get_footer_text(context):
    footer_text = ""
    if FooterText.objects.first() is not None:
        footer_text = FooterText.objects.first().body
        footer_url = FooterText.objects.first().url

    return {
        'footer_text': footer_text,
        'footer_url': footer_url,
    }

@register.inclusion_tag('blog/components/blog_tags_list.html', takes_context=True)
def blog_tags_list(context):
    tags = BlogPageTag.objects.all()
    return {
        'request': context['request'],
        'tags': tags
    }

@register.inclusion_tag('blog/components/news_list.html', takes_context=True)
def news_list(context):
    noticias = NewsPage.objects.all()
    return {
        'request': context['request'],
        'noticias': noticias
    }