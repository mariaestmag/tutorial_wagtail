from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register)

from libros.models import Libro


class LibrosAdmin(ModelAdmin):
    model = Libro
    search_fields = ('title', 'author', 'summary')
    menu_icon = 'fa-book'
    menu_order = 200  
    list_display = ('title','summary', 'imagen')


class LibrosAdminGroup(ModelAdminGroup):
    menu_label = 'Libros'
    menu_icon = 'fa-book'
    menu_order = 200  
    items = (LibrosAdmin,)

modeladmin_register(LibrosAdminGroup)
