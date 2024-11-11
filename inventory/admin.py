from django.contrib import admin
from .models import Item, Category, Supplier, SupplierItem, Transaction, TransactionItem, Project

class ItemAdmin(admin.ModelAdmin):
    exclude = ['itemCode']  #hiding itemCode from admin form since it's auto-generated
    list_display = ['itemName', 'itemQuantity', 'itemCode', 'itemCategory']

admin.site.register(Item, ItemAdmin)
admin.site.register(Category)
admin.site.register(Supplier)
admin.site.register(SupplierItem)
admin.site.register(Transaction)
admin.site.register(TransactionItem)
admin.site.register(Project)