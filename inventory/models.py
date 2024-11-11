from django.db import models, transaction
from math import ceil

##**********Need to update: itemCode and iteQuamtity in same not feasible without multiple body table || check admin panel*************

class Item(models.Model):
    itemName = models.CharField(max_length=30)
    itemQuantity = models.PositiveIntegerField(default=1)
    itemCode = models.CharField(max_length=5, unique=True, editable=False)
    itemCategory = models.ForeignKey('Category', on_delete=models.PROTECT) #protects the category from being deleted before all items are deleted
    
    #auto generation of item code when each instance is saved
    def save(self, *args, **kwargs):
        if not self.itemCode:
            prefix = self.itemName[:2].capitalize()
            
            #searching if item code with that prefix already exists
            last_item = Item.objects.filter(itemCode__startswith=prefix).order_by('-itemCode').first() #sorting in desc order to find the most recent one(if exists)
            #if exists, goes to if, else creating a new code with code = {prefix}01
            if last_item:
                #extract number part regardless of length
                number_part = last_item.itemCode[2:] #skipping 2 index, hence starts from numbers
                last_number = int(number_part)
                new_number = last_number + 1
                
                #determining format based on number size, after no of items of same type increases past 99, using 3 digits
                if new_number <= 99:
                    self.itemCode = f"{prefix}{new_number:02d}" #02d: format specifier for consistent code, turns Ra2 to Ra02
                else:
                    self.itemCode = f"{prefix}{new_number:03d}"  #using 3 digits after 99
            else:
                self.itemCode = f"{prefix}01"
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.itemName}"

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
        return f"{self.supplier.supplierName} - {self.item.itemName}"

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
        return f"{self.transaction.billNo} - {self.item.itemName}"

class Transaction(models.Model):
    billNo = models.CharField(max_length=30, unique=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT)
    totalPrice = models.PositiveIntegerField(editable=False, null=True, blank=True)
    finalPriceWithVat = models.PositiveIntegerField(editable=False, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        #only calculate if transaction instance exists
        if self.pk:
            items = TransactionItem.objects.filter(transaction=self) #retrieving all the related TransactionItem objects
            self.totalPrice = sum(item.quantity * item.price for item in items) #sum of quantity * price
            self.finalPriceWithVat = ceil(1.13 * self.totalPrice) #ceil is a function of math library 
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.billNo

class Project(models.Model):
    projectName = models.CharField(max_length=40)
    projectLeader = models.CharField(max_length=30)
    items = models.ManyToManyField(Item)
    
    def __str__(self):
        return self.projectName