from django.contrib import admin
from .models import Item, IndividualItem, Category, Supplier, SupplierItem, Transaction, TransactionItem, Project

class SupplierItemInline(admin.TabularInline):
    model = SupplierItem
    extra = 1

class TransactionItemInline(admin.TabularInline):
    model = TransactionItem
    extra = 1

class IndividualItemInline(admin.TabularInline):
    model = IndividualItem
    readonly_fields = ('itemCode',)
    extra = 0
    can_delete = False
    max_num = 0  #prevent adding through inline
    show_change_link = True

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('itemName', 'itemQuantity', 'available_quantity', 'itemCategory')
    search_fields = ('itemName',)
    list_filter = ('itemCategory',)
    inlines = [IndividualItemInline]

@admin.register(IndividualItem)
class IndividualItemAdmin(admin.ModelAdmin):
    list_display = ('itemCode', 'item', 'is_available', 'price')
    search_fields = ('itemCode', 'item__itemName')
    list_filter = ('is_available', 'item')
    readonly_fields = ('itemCode',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('categoryName', 'categoryQuantity')
    search_fields = ('categoryName',)

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('supplierName', 'address', 'contactNo')
    search_fields = ('supplierName',)
    inlines = [SupplierItemInline]

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('billNo', 'supplier', 'totalPrice', 'finalPriceWithVat', 'date', 'paymentStatus')
    search_fields = ('billNo', 'supplier__supplierName')
    list_filter = ('date', 'supplier', 'paymentStatus')
    readonly_fields = ('totalPrice', 'finalPriceWithVat')
    inlines = [TransactionItemInline]

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('projectName', 'projectLeader')
    search_fields = ('projectName', 'projectLeader')
    filter_horizontal = ('items',)