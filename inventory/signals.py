from django.db.models.signals import post_delete, post_save
from django.db.models import Sum, F
from django.db import transaction
from django.db.utils import DatabaseError
from django.dispatch import receiver
from math import ceil
from inventory.models import TransactionItem, Category, Item, Transaction
# from inventory_management.utils import api_response

###here, instance is being used instead of self, as we're working with instance of Transcation and not of signal###
@receiver([post_save, post_delete], sender=TransactionItem)
def update_transaction(sender, instance, created=None, **kwargs):
    try:
        with transaction.atomic(): #ensuring atomicity(so that all calculations are implemented at once and if error occurs, it's rolled back)
            if hasattr(instance, 'transaction') and instance.transaction:
                #first checking if the instance has attribute transaction, and secondly checking if the instance has a truthy value(meaning value exists and is not false, null, 0 or an empty string)
                #hasattr is redundant remove later
                transaction_instance = instance.transaction

                ####This is another approach but has a bottleneck for large datasets; memory inefficient####
                # related_items = TransactionItem.objects.filter(transaction=transaction_instance) #retreiving items that belong to current instance and is TransactionItems' object
                # #keyword argument for filter is name of model field(in this case is the foreign key field) and value is value you're filtering by
                # if related_items.exists():
                #     #checking if any items exists in current instance
                #     totalPrice = sum(item.quantity * item.price for item in related_items)
                #     finalPriceWithVat = ceil(totalPrice * 1.13)
                # else:
                #     #if not, by default, 0
                #     totalPrice = 0
                #     finalPriceWithVat = 0

                #retreiving items that belong to current instance and is TransactionItems' object
                #aggregating the total price directly in the database
                result = TransactionItem.objects.filter(transaction=transaction_instance).aggregate(
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

    except DatabaseError as db_error:
        raise Exception(f"Error while updating transaction: {str(db_error)}")
    except Exception as e:
        print(f"Unexpected error: {e}")

@receiver([post_save, post_delete], sender=Item)
def update_category_on_quantity_and_delete_individual_items(sender, instance, created=None, **kwargs): 
    # created=None for handling both post_save and delete. For delete, it won't cause any problems by being none, and for save, it's automatically assigned
    try:
        with transaction.atomic():
            # filtering items to be of the same category as of the current instance
            filtered_items = Item.objects.filter(itemCategory=instance.itemCategory) 
            # itemCategory=instance just doing this will cause a ValueError as itemCategory=instance means you're trying to filter by exact value the current instance has, e.g., "Raspberry Pi", instead of the category of said item
            # summing at the database level
            aggregated_result = filtered_items.aggregate(Sum('itemQuantity'))
            # aggregate returns a dict, and total quantity is in key - itemQuantity__sum, but when filtering it could be empty so to handle None, else condition has a fallback to 0
            total_quantity = aggregated_result['itemQuantity__sum'] if aggregated_result['itemQuantity__sum'] is not None else 0
            # updating categoryQuantity to calculated quantity
            Category.objects.filter(pk=instance.itemCategory.pk).update(categoryQuantity=total_quantity)
            
            if created is None:
                instance.individual_items.all().delete()
    except Exception as e:
        raise Exception(f"Error while processing item update or deletion: {e}")

#****sometimes working and sometimes not*****
@receiver([post_save, post_delete], sender=TransactionItem)
def update_available_quantity_from_transactionitem_change(sender, instance, created=None, **kwargs):
    with transaction.atomic():
        try:
            #making sure category matches before updating
            if instance.item.itemCategory != instance.category:
                raise ValueError(f"Item category mismatch for: {instance.item.itemName}")
            
            if kwargs.get('signal') == post_save:
                if created:  #if the TransactionItem is newly created, adding the quantity to the Item
                    instance.item.itemQuantity += instance.quantity
                else:  #if the TransactionItem is updated, getting the previous quantity before updating
                    previous_quantity = instance.__class__.objects.get(pk=instance.pk).quantity
                    instance.item.itemQuantity += instance.quantity - previous_quantity

            elif kwargs.get('signal') == post_delete:
                #subtracting the quantity if a TransactionItem is deleted
                instance.item.itemQuantity -= instance.quantity

            instance.item.save()
                
        except Exception as e:
            raise Exception(f"Error while updating item quantity from transactionitem: {e}")
        
@receiver(post_delete, sender=Transaction)
def update_transaction_on_transactionitem_delete(sender, instance, **kwargs):
    try:
        instance.transactionitem_transaction.all().delete()
    except Exception as e:
        raise Exception(f"Couldn't delete: {e}")