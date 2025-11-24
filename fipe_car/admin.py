from django.contrib import admin
from .models import FipeCar

class FipeCarAdmin(admin.ModelAdmin):
    list_display = ('fipe_id', 'brand', 'model', 'year', 'fuel_type', 'gear_type', 'engine_size', 'price')
    
    search_fields = ('fipe_id', 'brand', 'model')
    
    list_filter = ('brand', 'model', 'year', 'fuel_type', 'gear_type')
    
    ordering = ('brand', 'model', 'year')
     
    fieldsets = (
        (None, {
            'fields': ('fipe_id', 'brand', 'model', 'year', 'fuel_type', 'gear_type', 'engine_size', 'price')
        }),
    )
    
admin.site.register(FipeCar, FipeCarAdmin)