from django.contrib import admin
from django.forms.widgets import Select
from django.db.models import Q
from .models import *

class SupplierItemInline(admin.TabularInline):
    model = SupplierItem
    extra = 1

class PurchaseItemInline(admin.TabularInline):
    model = PurchaseItem
    extra = 1

class IndividualItemInline(admin.TabularInline):
    model = IndividualItem
    readonly_fields = ('itemCode',)
    extra = 0
    can_delete = False
    max_num = 0  #preventing adding through inline
    show_change_link = True

class ProjectItemInline(admin.TabularInline):
    model = ProjectItem
    extra = 1 #1 means show 1 more fields to add without clicking add another, 0 means none
    autocomplete_fields = ['item'] #shows dropdown
    exclude = ['individual_items']

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

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('billNo', 'supplier', 'totalPrice', 'finalPriceWithVat', 'date', 'paymentStatus')
    search_fields = ('billNo', 'supplier__supplierName')
    list_filter = ('date', 'supplier', 'paymentStatus')
    readonly_fields = ('totalPrice', 'finalPriceWithVat')
    inlines = [PurchaseItemInline]

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('projectName', 'projectLeader')
    search_fields = ('projectName', 'projectLeader')
    inlines = [ProjectItemInline]

@admin.register(ProjectItem)
class ProjectItemAdmin(admin.ModelAdmin):
    list_display = ('associated_project', 'item', 'quantity', 'start_date')
    search_fields = ('project__projectName', 'item__itemName')
    list_filter = ('associated_project', 'item')
    readonly_fields = ('start_date',)
    
    def get_queryset(self, request):
        #optimizing the queryset by selecting related fields
        return super().get_queryset(request).select_related('associated_project', 'item')
