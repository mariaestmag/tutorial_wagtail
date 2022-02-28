from leaflet.admin import LeafletGeoAdmin
from django.contrib import admin
from blog.models import TravelPage

admin.site.register(TravelPage, LeafletGeoAdmin)