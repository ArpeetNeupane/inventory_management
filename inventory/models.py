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
    
    def save(self, *args, **kwargs):
        is_new = self.pk is None  #this checks if the pk attribute is None. If it is, the instance has not been
        #saved to the database yet, meaning it's a new instance.
        
        #if self.pk is none, the code below is triggered, else old_quantity doesn't exist hence it becomes 0, simple ternary operator
        #if old_quantity exists, fit queries the database to get the current itemQuantity of this item and flat=True makes sure its a list and not list of tuples
        #first() is used because i) if queryset is empty, returns none instead of exception so separate exception handeling is not needed
        #converts from queryset (which is iterable) to actual value. if get was used, have to have a separate exception handeling logic
        old_quantity = Item.objects.filter(pk=self.pk).values_list('itemQuantity', flat=True).first() if self.pk else 0
        #saving the main item
        super().save(*args, **kwargs)
        
        if is_new:
            #generating codes for all new items
            self._generate_individual_codes(self.itemQuantity)
        elif self.itemQuantity > old_quantity:
            #generating additional codes if quantity increased
            additional_quantity = self.itemQuantity - old_quantity
            self._generate_individual_codes(additional_quantity)
        elif self.itemQuantity < old_quantity:
            #removing excess codes if quantity decreased
            excess_items = self.individual_items.filter(is_available=True).order_by('-itemCode')[old_quantity - self.itemQuantity:] #add exception for when is_available is false
            excess_items.delete()

    def _generate_individual_codes(self, quantity):
        #extracting the first two letters of the itemName and converting them to uppercase to form a prefix for the unique code.
        prefix = self.itemName[:2].upper() #:2 means taking 2 characters from start
        
        #getting the last used number for this prefix
        last_item = IndividualItem.objects.filter(
            itemCode__startswith=prefix
        ).order_by('-itemCode').first() #checking from highest; descending order, and taking first value

        #if previous code doesn't exist, starts at 1
        start_number = 1
        if last_item:
            #if a previous code exists, extracting the last most number, converting to int and increasing by 1
            number_part = last_item.itemCode[2:] #2: means taking after 2 characters from start
            start_number = int(number_part) + 1

        #creating individual items with unique codes (in bulk if required)
        individual_items = []
        for i in range(quantity):
            number = start_number + i
            #using 4 digits for the number part (allowing up to 9999 items)
            item_code = f"{prefix}{number:04d}" #unique code syntax = prefix + 4 digit number. eg: if Raspberry Pi's 10th item, code = RA0010

            #creating individual_item object but not saving to database yet
            individual_items.append(IndividualItem(
                item=self, #linking IndividualItem to the current Item instance
                itemCode=item_code #assigning generated code
            ))
        #saving at bult to database (efficient)
        IndividualItem.objects.bulk_create(individual_items)

    def __str__(self):
        return f"{self.itemName}"

    #allows it to be accessed like an attribute (eg: item.available_quantity without paranthesis) without explicitly calling it as a method; read-only property
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
     
    def save(self, *args, **kwargs):
        #only calculate if transaction instance exists
        if self.pk:
            items = TransactionItem.objects.filter(transaction=self) #retrieving all the related TransactionItem objects
            self.totalPrice = sum(item.quantity * item.price for item in items) #sum of quantity * price
            self.finalPriceWithVat = ceil(1.13 * self.totalPrice) #ceil(ceiling) is a function of math library for rounding up
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.billNo

class Project(models.Model):
    projectName = models.CharField(max_length=40)
    projectLeader = models.CharField(max_length=30)
    items = models.ManyToManyField(Item)
    
    def __str__(self):
        return self.projectName