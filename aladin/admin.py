from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(item)
class itemAdmin(admin.ModelAdmin):
    list_display = ('namee', 'cat_name', 'price')

@admin.register(cart)
class cartAdmin(admin.ModelAdmin):
    list_display = ('name','item_name', 'quantity', 'price')

@admin.register(order)
class orderAdmin(admin.ModelAdmin):
    list_display = ('name', 'addressa','ordered')

admin.site.register(troy)
admin.site.register(address)
admin.site.register(category)