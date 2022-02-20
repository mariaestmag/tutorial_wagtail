from blog.models import BlogCategory as Category
from blog.models import FooterText
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