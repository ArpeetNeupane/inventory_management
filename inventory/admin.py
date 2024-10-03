from django.contrib import admin
from .models import Items, Categories

class ItemsAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'quantity', 'category', 'price', 'bill_no', 'supplier', 'date')
    readonly_fields = ('date',)  #making 'date' visible but not editable

admin.site.register(Items, ItemsAdmin)
admin.site.register(Categories)

