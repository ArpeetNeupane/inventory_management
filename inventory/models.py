from django.db import models
from math import ceil

class IndividualItem(models.Model):
    item = models.ForeignKey('Item', on_delete=models.CASCADE, related_name='individual_items') #related name is a property that allows items to be searched using that name (here, item belongs to what what items with their codes)
    #default related name is individualitem_set
    itemCode = models.CharField(max_length=6, unique=True)
    is_available = models.BooleanField(default=True)  #to track if item is assigned/used

    def __str__(self):
        return f"{self.item.itemName}"

class Item(models.Model):
    itemName = models.CharField(max_length=30)
    itemQuantity = models.PositiveIntegerField(default=1)
    itemCategory = models.ForeignKey('Category', on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.itemName}"

    #@property allows it to be accessed like an attribute (eg: item.available_quantity without paranthesis) without explicitly calling it as a method; read-only property
    #provides encapsulation and easier access to users
    @property
    def available_quantity(self):
        return self.individual_items.filter(is_available=True).count() #accessing related items because of foreign key through self.individual_items which is the related name, counting no of available items

class Category(models.Model):
    categoryName = models.CharField(max_length=30, unique=True)
    categoryQuantity = models.PositiveIntegerField()
    
    def __str__(self):
        return self.categoryName

class SupplierItem(models.Model):
    supplier = models.ForeignKey('Supplier', on_delete=models.CASCADE)
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    supply_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.supplier.supplierName

class Supplier(models.Model):
    supplierName = models.CharField(max_length=30)
    address = models.CharField(max_length=40)
    contactNo = models.CharField(max_length=15)
    items = models.ManyToManyField(Item, through='SupplierItem')
    #many-to-many relationship between Supplier model and the Item model,using an intermediary model - SupplierItem
    def __str__(self):
        return self.supplierName

class TransactionItem(models.Model):
    transaction = models.ForeignKey('Transaction', on_delete=models.CASCADE)
    item = models.ForeignKey('Item', on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    
    def __str__(self):
        return self.transaction.billNo

class Transaction(models.Model):
    billNo = models.CharField(max_length=30, unique=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT)
    totalPrice = models.PositiveIntegerField(editable=False, null=True, blank=True)
    finalPriceWithVat = models.PositiveIntegerField(editable=False, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    paymentStatus = models.CharField(max_length=8, default='Pending') #paid or not paid/pending
    
    def __str__(self):
        return self.billNo

class Project(models.Model):
    projectName = models.CharField(max_length=40)
    projectLeader = models.CharField(max_length=30)
    items = models.ManyToManyField(Item)
    
    def __str__(self):
        return self.projectName