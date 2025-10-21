from django.contrib import admin
from django.utils.html import format_html
from unfold import admin as unfold_admin
from .models import Region, Client, Color, ClientType, Category, Check, Karniz, Selpe


@admin.register(Region)
class RegionAdmin(unfold_admin.ModelAdmin):
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


@admin.register(Category)
class CategoryAdmin(unfold_admin.ModelAdmin):
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
class ClientAdmin(unfold_admin.ModelAdmin):
    list_display = ('id', 'name', 'region', 'client_type', 'wallet', 'formatted_created_at', 'formatted_updated_at')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'region__name', 'client_type__type')
    list_filter = ('region', 'client_type', 'created_at', 'updated_at')
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
            'fields': ('name', 'region', 'client_type')
        }),
        ('Финансовая информация', {
            'fields': ('wallet',)
        }),
    )
    
    # Add autocomplete for foreign keys
    autocomplete_fields = ['region', 'client_type']


@admin.register(ClientType)
class ClientTypeAdmin(unfold_admin.ModelAdmin):
    list_display = ('id', 'type', 'formatted_created_at', 'formatted_updated_at')
    list_display_links = ('id', 'type')
    search_fields = ('type',)
    list_filter = ('created_at', 'updated_at')
    ordering = ('type',)
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
        ('Информация о типе клиента', {
            'fields': ('type',)
        }),
    )


@admin.register(Color)
class ColorAdmin(unfold_admin.ModelAdmin):
    list_display = ('id', 'kod', 'category', 'mary_diller_USD', 'mary_diller_TMT', 'formatted_created_at', 'formatted_updated_at')
    list_display_links = ('id', 'kod')
    search_fields = ('kod', 'category__name')
    list_filter = ('category', 'created_at', 'updated_at')
    ordering = ('kod',)
    readonly_fields = ('formatted_created_at', 'formatted_updated_at')
    list_per_page = 100
    autocomplete_fields = ['category']
    
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
            'fields': ('kod', 'category')
        }),
        ('Mary diller', {
            'fields': ('mary_diller_USD', 'mary_diller_TMT'),
            'classes': ('collapse',)
        }),
        ('Diller', {
            'fields': ('diller_USD', 'diller_TMT'),
            'classes': ('collapse',)
        }),
        ('Bez ustanowka', {
            'fields': ('bez_ustanowka_USD', 'bez_ustanowka_TMT'),
            'classes': ('collapse',)
        }),
        ('Mata', {
            'fields': ('mata_USD', 'mata_TMT'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Check)
class CheckAdmin(unfold_admin.ModelAdmin):
    list_display = ('id', 'client', 'price', 'colored_status', 'formatted_created_at', 'formatted_updated_at')
    list_display_links = ('id', 'client')
    search_fields = ('client__name',)
    list_filter = ('status', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    readonly_fields = ('formatted_created_at', 'formatted_updated_at', 'colored_status')
    list_per_page = 50
    autocomplete_fields = ['client']
    
    def colored_status(self, obj):
        """Display status with color coding"""
        color_map = {
            'inactive': '#95a5a6',  # Gray
            'process': '#f39c12',   # Orange
            'done': '#27ae60'       # Green
        }
        
        status_labels = {
            'inactive': 'Inactive',
            'process': 'Process',
            'done': 'Done'
        }
        
        color = color_map.get(obj.status, '#95a5a6')
        label = status_labels.get(obj.status, obj.status)
        
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px 12px; border-radius: 4px; font-weight: 600; font-size: 0.85rem; display: inline-block;">{}</span>',
            color,
            label
        )
    colored_status.short_description = 'Статус'
    colored_status.admin_order_field = 'status'
    
    def formatted_created_at(self, obj):
        return obj.created_at.strftime('%d.%m.%Y %H:%M')
    formatted_created_at.short_description = 'Создан'
    formatted_created_at.admin_order_field = 'created_at'
    
    def formatted_updated_at(self, obj):
        return obj.updated_at.strftime('%d.%m.%Y %H:%M')
    formatted_updated_at.short_description = 'Обновлен'
    formatted_updated_at.admin_order_field = 'updated_at'
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('client', 'file')
        }),
        ('Финансовая информация', {
            'fields': ('price',)
        }),
        ('Статус', {
            'fields': ('status',)
        }),
    )


@admin.register(Karniz)
class KarnizAdmin(unfold_admin.ModelAdmin):
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
        ('Информация о карнизе', {
            'fields': ('name',)
        }),
    )


@admin.register(Selpe)
class SelpeAdmin(unfold_admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'formatted_created_at', 'formatted_updated_at')
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
        ('Информация о шелпе', {
            'fields': ('name', 'price')
        }),
    )
