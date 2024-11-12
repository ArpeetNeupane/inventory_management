from django.db import models, transaction
from math import ceil

class IndividualItem(models.Model):
    item = models.ForeignKey('Item', on_delete=models.CASCADE, related_name='individual_items')
    itemCode = models.CharField(max_length=6, unique=True)
    is_available = models.BooleanField(default=True)  # To track if item is assigned/used

    def __str__(self):
        return f"{self.item.itemName} - {self.itemCode}"

class Item(models.Model):
    itemName = models.CharField(max_length=30)
    itemQuantity = models.PositiveIntegerField(default=1)
    itemCategory = models.ForeignKey('Category', on_delete=models.PROTECT)
    
    def save(self, *args, **kwargs):
        is_new = self.pk is None  # Check if this is a new item
        old_quantity = Item.objects.filter(pk=self.pk).values_list('itemQuantity', flat=True).first() if self.pk else 0
        
        # Save the main item first
        super().save(*args, **kwargs)
        
        if is_new:
            # Generate codes for all new items
            self._generate_individual_codes(self.itemQuantity)
        elif self.itemQuantity > old_quantity:
            # Generate additional codes if quantity increased
            additional_quantity = self.itemQuantity - old_quantity
            self._generate_individual_codes(additional_quantity)
        elif self.itemQuantity < old_quantity:
            # Remove excess codes if quantity decreased
            excess_items = self.individual_items.filter(
                is_available=True
            ).order_by('-itemCode')[:old_quantity - self.itemQuantity]
            excess_items.delete()

    def _generate_individual_codes(self, quantity):
        prefix = self.itemName[:2].upper()
        
        # Get the last used number for this prefix
        last_item = IndividualItem.objects.filter(
            itemCode__startswith=prefix
        ).order_by('-itemCode').first()

        start_number = 1
        if last_item:
            # Extract the number part and increment
            number_part = last_item.itemCode[2:]
            start_number = int(number_part) + 1

        # Create individual items with unique codes
        individual_items = []
        for i in range(quantity):
            number = start_number + i
            # Use 4 digits for the number part (allowing up to 9999 items)
            item_code = f"{prefix}{number:04d}"
            individual_items.append(IndividualItem(
                item=self,
                itemCode=item_code
            ))
        
        IndividualItem.objects.bulk_create(individual_items)

    def __str__(self):
        return f"{self.itemName}"

    @property
    def available_quantity(self):
        return self.individual_items.filter(is_available=True).count()

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