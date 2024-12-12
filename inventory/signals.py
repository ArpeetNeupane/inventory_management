from django.db.models.signals import post_delete, post_save, pre_save
from django.db.models import Sum, F
from django.db import transaction
from django.db.utils import DatabaseError
from django.dispatch import receiver
from math import ceil
from inventory.models import TransactionItem, Category, Item, Transaction, SupplierItem, IndividualItem
# from inventory_management.utils import api_response

#price update from item creation
#supplier le tyo item sell gardaina vane exception

#capturing old quantity of TransactionItem
@receiver(pre_save, sender=TransactionItem)
def capture_original_quantities(sender, instance, **kwargs):
    #checking if old or new instances, only doing this for existing instances
    if instance.pk:
        try:
            #storing original quantities for all items in transaction_items, filter: items filtered are of the same transaction as as transaction of current instance
            transaction_items = TransactionItem.objects.filter(transaction=instance.transaction)
            
            #dictionary to store original quantities
            original_quantities = {}
            for trans_item in transaction_items:
                #storing quantity of current TransactionItem
                original_quantities[trans_item.pk] = trans_item.quantity
            
            #attaching to the instance as a temporary attribute
            instance._original_quantities = original_quantities
        except Exception as e:
            instance._original_quantities = {}

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

    try:
        with transaction.atomic():
                #making sure category matches before updating
                if instance.item.itemCategory != instance.category:
                    raise ValueError(f"Item category mismatch for: {instance.item.itemName}")
                
                #making sure current item being added to transaction item with said supplier supplies the item, if not, exception raised
                #getting the supplier of the transaction
                transaction_supplier = instance.transaction.supplier

                is_supplied = SupplierItem.objects.filter(
                    supplier=transaction_supplier, 
                    item=instance.item
                ).exists()

                if not is_supplied:
                    raise Exception(f"{transaction_supplier.supplierName} doesn't supply the item {instance.item.itemName}.")
                
                transaction_items = TransactionItem.objects.filter(transaction=instance.transaction)

                if kwargs.get('signal') == post_save:   
                    if created:  #if the TransactionItem is newly created, adding the quantity to the Item
                        print("Newly Created!")

                        #updating quantity
                        instance.item.itemQuantity += instance.quantity
                        instance.item.save()

                        #updating prices according to inputted price during TransactionItem creation
                        #filtering all individual items for this item, which matches the instance and is_available
                        individual_items = IndividualItem.objects.filter(
                            item=instance.item, 
                            is_available=True
                        ).order_by('itemCode')[:instance.quantity] #slicing to only the number of quantity the same as when creating TransactionItem so as to not overload
                        
                        #updating prices for these individual items
                        try:
                            for ind_item in individual_items:
                                ind_item.price = instance.price
                                ind_item.save(update_fields=['price'])
                        
                        except Exception as e:
                            print(f"Error updating individual item prices: {e}")

                    else:  #if the TransactionItem is updated, getting the previous quantity before updating
                        print("Not Newly Created but updated!")
                        #first, getting original quantity from pre_save
                        original_quantities = getattr(instance, '_original_quantities', {}) #default is {} if no value

                        for trans_item in transaction_items:
                        #if item is being updated, calculate quantity difference
                            if trans_item.pk == instance.pk:
                                original_quantity = original_quantities.get(trans_item.pk, trans_item.quantity)
                                #get(trans_item.pk, trans_item.quantity) 
                                quantity_diff = instance.quantity - original_quantity
                                
                                #updating quantity
                                trans_item.item.itemQuantity += quantity_diff
                                trans_item.item.save()

                                #updating prices according to inputted price during TransactionItem creation
                                #filtering all individual items for this item, which matches the instance and is_available
                                individual_items = IndividualItem.objects.filter(
                                    item=trans_item.item, 
                                    is_available=True
                                ).order_by('itemCode')[:instance.quantity]
                                
                                #updating prices for these individual items
                                for ind_item in individual_items:
                                    ind_item.price = instance.price
                                    ind_item.save(update_fields=['price'])
                            
                            else:
                                print("Wrong Instance")

                elif kwargs.get('signal') == post_delete:
                    print("Newly Deleted!")
                    #subtracting the quantity if a TransactionItem is deleted
                        
                    instance.item.itemQuantity -= instance.quantity
                    instance.item.save()
                
    except Exception as e:
        raise Exception(f"Error while updating item quantity from transactionitem: {e}")

@receiver([post_save, post_delete], sender=Item)
def update_category_on_quantity_and_delete_individual_items(sender, instance, created=None, **kwargs): 
    #created=None for handling both post_save and delete. For delete, it won't cause any problems by being none, and for save, it's automatically assigned
    try:
        with transaction.atomic():
            #filtering items to be of the same category as of the current instance
            filtered_items = Item.objects.filter(itemCategory=instance.itemCategory) 
            #itemCategory=instance just doing this will cause a ValueError as itemCategory=instance means you're trying to filter by exact value the current instance has, e.g., "Raspberry Pi", instead of the category of said item
            #summing at the database level
            aggregated_result = filtered_items.aggregate(Sum('itemQuantity'))
            #aggregate returns a dict, and total quantity is in key - itemQuantity__sum, but when filtering it could be empty so to handle None, else condition has a fallback to 0
            total_quantity = aggregated_result['itemQuantity__sum'] if aggregated_result['itemQuantity__sum'] is not None else 0
            #updating categoryQuantity to calculated quantity
            Category.objects.filter(pk=instance.itemCategory.pk).update(categoryQuantity=total_quantity)
            
            if created is None:
                instance.individual_items.all().delete()
    except Exception as e:
        raise Exception(f"Error while processing item update or deletion: {e}")
        
@receiver(post_delete, sender=Transaction)
def update_transaction_on_transactionitem_delete(sender, instance, **kwargs):
    try:
        instance.transactionitem_transaction.all().delete()
    except Exception as e:
        raise Exception(f"Couldn't delete: {e}")
    
#project ma lida exact opposite of transaction item and handle price correcly during transactionitem of a supplier