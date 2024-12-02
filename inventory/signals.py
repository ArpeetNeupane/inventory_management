from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.db import transaction
from math import ceil
from .models import TransactionItem, Item, IndividualItem
from django.db.models import Sum, F

###here, instance is being used instead of self, as we're working with instance of Transcation and not of signal###
@receiver([post_save, post_delete], sender=TransactionItem)
def update_transaction(sender, instance, **kwargs):
    with transaction.atomic(): #ensuring atomicity(so that all calculations are implemented at once and if error occurs, it's rolled back)
        if hasattr(instance, 'transaction') and instance.transaction:
            #first checking if the instance has attribute transaction, and secondly checking if the instance has a truthy value(meaning value exists and is not false, null,0 or an empty string)
            transaction_instance = instance.transaction

            related_items = TransactionItem.objects.filter(transaction=transaction_instance) #retreiving items that belong to current instance and is TransactionItems' object

            ####This is another approach but has a bottleneck for large datasets; memory inefficient####

            # #keyword argument for filter is name of model field(in this case is the foreign key field) and value is value you're filtering by
            # if related_items.exists():
            #     #checking if any items exists in current instance
            #     totalPrice = sum(item.quantity * item.price for item in related_items)
            #     finalPriceWithVat = ceil(totalPrice * 1.13)
            # else:
            #     #if not, by default, 0
            #     totalPrice = 0
            #     finalPriceWithVat = 0

            #aggregating the total price directly in the database
            result = related_items.aggregate(
                total_price=Sum(F('quantity') * F('price')) #F allows you to reference model field values directly in database queries
                #aggregate --> basically means that the multiplication happens efficiently at the database level, avoiding the need to load the entire dataset into memory and perform the operation in Python
            )
            
            #extracting the total price from the result dictionary (defaulting to 0 if there's no result)
            totalPrice = result['total_price'] or 0
            
            # Calculate the final price with VAT
            finalPriceWithVat = ceil(totalPrice * 1.13)

            transaction_instance.totalPrice = totalPrice
            transaction_instance.finalPriceWithVat = finalPriceWithVat
            transaction_instance.save(update_fields=['totalPrice', 'finalPriceWithVat'])

@receiver(post_save, sender=Item)
def update_items(sender, instance, **kwargs):
    pass

# def save(self, *args, **kwargs):
#         is_new = self.pk is None  #this checks if the pk attribute is None. If it is, the instance has not been
#         #saved to the database yet, meaning it's a new instance.
        
#         #if self.pk is none, the code below is triggered, else old_quantity doesn't exist hence it becomes 0, simple ternary operator
#         #if old_quantity exists, fit queries the database to get the current itemQuantity of this item and flat=True makes sure its a list and not list of tuples
#         #first() is used because i) if queryset is empty, returns none instead of exception so separate exception handeling is not needed
#         #converts from queryset (which is iterable) to actual value. if get was used, have to have a separate exception handeling logic
#         old_quantity = Item.objects.filter(pk=self.pk).values_list('itemQuantity', flat=True).first() if self.pk else 0
#         #saving the main item
#         super().save(*args, **kwargs)
        
#         if is_new:
#             #generating codes for all new items
#             self._generate_individual_codes(self.itemQuantity)
#         elif self.itemQuantity > old_quantity:
#             #generating additional codes if quantity increased
#             additional_quantity = self.itemQuantity - old_quantity
#             self._generate_individual_codes(additional_quantity)
#         elif self.itemQuantity < old_quantity:
#             #removing excess codes if quantity decreased
#             excess_quantity = old_quantity - self.itemQuantity

#             #materializing queryset into a list to avoid slicing issues with delete()
#             excess_items = list(
#                 self.individual_items.filter(is_available=True)
#                 .order_by('-itemCode')[:excess_quantity]
#             )
#             #here, if item code exists till RA60 and RA57 and RA58 aren't available, and 4 are deleted, RA 59, 60, 55, 56 are deleted.

#             #iterating over and deleting the excess items
#             for item in excess_items:
#                 item.delete()

#     def _generate_individual_codes(self, quantity):
#         #extracting the first two letters of the itemName and converting them to uppercase to form a prefix for the unique code.
#         prefix = self.itemName[:2].upper() #:2 means taking 2 characters from start
        
#         #getting the last used number for this prefix
#         last_item = IndividualItem.objects.filter(
#             itemCode__startswith=prefix
#         ).order_by('-itemCode').first() #checking from highest; descending order, and taking first value

#         #if previous code doesn't exist, starts at 1
#         start_number = 1
#         if last_item:
#             #if a previous code exists, extracting the last most number, converting to int and increasing by 1
#             number_part = last_item.itemCode[2:] #2: means taking after 2 characters from start
#             start_number = int(number_part) + 1

#         #creating individual items with unique codes (in bulk if required)
#         individual_items = []
#         for i in range(quantity):
#             number = start_number + i
#             #using 4 digits for the number part (allowing up to 9999 items)
#             item_code = f"{prefix}{number:04d}" #unique code syntax = prefix + 4 digit number. eg: if Raspberry Pi's 10th item, code = RA0010

#             #creating individual_item object but not saving to database yet
#             individual_items.append(IndividualItem(
#                 item=self, #linking IndividualItem to the current Item instance
#                 itemCode=item_code #assigning generated code
#             ))
#         #saving at bult to database (efficient)
#         IndividualItem.objects.bulk_create(individual_items)