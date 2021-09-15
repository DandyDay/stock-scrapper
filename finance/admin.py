from django.contrib import admin

# Register your models here.

from .models import Stock, StockCategory


class StockInline(admin.TabularInline):
    model = Stock
    extra = 3


class StockCategoryAdmin(admin.ModelAdmin):
    fields = ['category_name', 'category_name_display']
    inlines = [StockInline]


admin.site.register(StockCategory, StockCategoryAdmin)
