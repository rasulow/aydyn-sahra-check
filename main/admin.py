from django.contrib import admin
from .models import Region, Client, Color


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'formatted_created_at', 'formatted_updated_at')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    list_filter = ('created_at', 'updated_at')
    ordering = ('name',)
    readonly_fields = ('formatted_created_at', 'formatted_updated_at')
    
    def formatted_created_at(self, obj):
        return obj.created_at.strftime('%d.%m.%Y')
    formatted_created_at.short_description = 'Создан'
    formatted_created_at.admin_order_field = 'created_at'
    
    def formatted_updated_at(self, obj):
        return obj.updated_at.strftime('%d.%m.%Y')
    formatted_updated_at.short_description = 'Обновлен'
    formatted_updated_at.admin_order_field = 'updated_at'
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name',)
        }),
    )


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'region', 'wallet', 'formatted_created_at', 'formatted_updated_at')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'region__name')
    list_filter = ('region', 'created_at', 'updated_at')
    ordering = ('name',)
    readonly_fields = ('formatted_created_at', 'formatted_updated_at')
    list_per_page = 50
    
    def formatted_created_at(self, obj):
        return obj.created_at.strftime('%d.%m.%Y')
    formatted_created_at.short_description = 'Создан'
    formatted_created_at.admin_order_field = 'created_at'
    
    def formatted_updated_at(self, obj):
        return obj.updated_at.strftime('%d.%m.%Y')
    formatted_updated_at.short_description = 'Обновлен'
    formatted_updated_at.admin_order_field = 'updated_at'
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'region')
        }),
        ('Финансовая информация', {
            'fields': ('wallet',)
        }),
    )
    
    # Add autocomplete for foreign key
    autocomplete_fields = ['region']


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('id', 'kod', 'price', 'formatted_created_at', 'formatted_updated_at')
    list_display_links = ('id', 'kod')
    search_fields = ('kod',)
    list_filter = ('created_at', 'updated_at')
    ordering = ('kod',)
    readonly_fields = ('formatted_created_at', 'formatted_updated_at')
    list_per_page = 100
    
    def formatted_created_at(self, obj):
        return obj.created_at.strftime('%d.%m.%Y')
    formatted_created_at.short_description = 'Создан'
    formatted_created_at.admin_order_field = 'created_at'
    
    def formatted_updated_at(self, obj):
        return obj.updated_at.strftime('%d.%m.%Y')
    formatted_updated_at.short_description = 'Обновлен'
    formatted_updated_at.admin_order_field = 'updated_at'
    
    fieldsets = (
        ('Информация о цвете', {
            'fields': ('kod', 'price')
        }),
    )
