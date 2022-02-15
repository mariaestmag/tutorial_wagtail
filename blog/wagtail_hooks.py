from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register)

from blog.models import FooterText

class FooterTextAdmin(ModelAdmin):
    model = FooterText
    search_fields = ('body',)