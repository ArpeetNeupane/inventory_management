from django.db import transaction
from django.db import connection
from django.db.models.signals import post_delete, post_save, pre_save, pre_delete, m2m_changed
from django.db.models import Sum, F
from django.db.utils import DatabaseError
from django.dispatch import receiver
from math import ceil
from inventory.models import TransactionItem, Category, Item, Transaction, SupplierItem, IndividualItem, Project, ProjectItem
# from inventory_management.utils import api_response

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
                
                #first, getting the supplier of the transaction
                transaction_supplier = instance.transaction.supplier

                is_supplied = SupplierItem.objects.filter(
                    supplier=transaction_supplier, 
                    item=instance.item
                ).exists()

                if not is_supplied:
                    raise Exception(f"{transaction_supplier.supplierName} doesn't supply the item {instance.item.itemName}.")
                
                #making sure the item that the supplier sells is set to correct price by the user
                price_of_supplied_item = SupplierItem.objects.filter(
                    supplier = transaction_supplier,
                    item = instance.item
                ).first()
                
                if instance.price != price_of_supplied_item.price:
                    raise ValueError(f"Item price mismatch for: {instance.item.itemName}")
                
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
        
@receiver(pre_delete, sender=Transaction)
def update_transaction_on_transactionitem_delete(sender, instance, **kwargs):
    try:
        items_in_deleted_transaction = TransactionItem.objects.filter(transaction=instance) #here, transaction=instance and not transaction=instance.transaction as the sender is transaction itself and it most likely doesn't have field referring to itself (unless there is)
        
        for item_in_deleted_transaction in items_in_deleted_transaction:
            quantity_of_deleted_item = item_in_deleted_transaction.quantity
            print(quantity_of_deleted_item)
            #*****if in future, manually handling itemQuantity after deletion of transaction is needed, code here*******

    except Exception as e:
        raise Exception(f"Couldn't calculate changes in item quantity after deletion of transaction: {e}")

@receiver(post_delete, sender=Transaction)
def delete_transactionitems_when_transaction_delete(sender, instance, **kwargs):
    try:
        with transaction.atomic():
            instance.transactionitem_transaction.all().delete()

    except Exception as e:
        raise Exception(f"Couldn't delete Transaction Items when deleting Transacation: {e}")

#if you use the regular approach for many to many field, it wont work as the ManyToManyField hasn’t been populated yet
#and the reason for that is, first the project item object is saved then the many to many relationship in django
#so we use m2m_changed signal to handle updates to many to many relationships
#here, atomicity is handled by default
@receiver(m2m_changed, sender=ProjectItem.individual_items.through) #sender here refers to the intermediate table that links ProjectItem and IndividualItem models.
def validate_individual_items(sender, instance, action, reverse, model, pk_set, **kwargs):
    if action in ['post_add', 'post_remove']: #if action is called to m2m relationship before items are added, or after removing
        try:
            with transaction.atomic():
                selected_count = instance.individual_items.count()
                print(selected_count)

                #checking if the number of individual items matches the required quantity
                if selected_count != instance.quantity:
                    raise ValueError(
                        f"Number of individual items must exactly match the project quantity. "
                        f"Selected: {selected_count}, Exactly Required: {instance.quantity}"
                    )

        except ValueError as e:
            raise Exception(f"str{e}")

#already unavailable borrow garna khojda exception
@receiver([post_save, post_delete], sender=ProjectItem)
def borrow_item_for_project(sender, instance, created=None, **kwargs):
    print("Signal Triggered before try and atomicity")
    try:
        with transaction.atomic():
            print("Signal Triggered after try and atomicity")
            #triggered only if not delete, i.e.,created or updated
            if created is not None:
                print("Inside created is not none")
                #validating that all selected individual items belong to the chosen item
                item_instance = instance.item 

                if not all(individual_item.item == item_instance for individual_item in instance.individual_items.all()):
                    raise ValueError("One or more individual items do not belong to the selected item.")

                #changing selected individual items to unavailable
                try:
                    instance.individual_items.update(is_available=False)
                except Exception as e:
                    raise Exception(f"Couldn't update availability after creation or modification of Project Item: {e}")
                print("below is_available=False")
            
            else:
                #changing selected individual items to available if deleted
                for individual_item in instance.individual_items.all():
                    if individual_item.is_available == True:
                        raise Exception(f"Cannot borrow {instance.item.itemName} as it is already being borrowed.")
                    instance.individual_items.update(is_available=True)
                print("below is_available=True")

    except Exception as e:
        raise Exception(f"Unknown Error: {e}")
    
@receiver(post_delete, sender=Project)
def delete_projectitems_when_project_delete(sender, instance, **kwargs):
    try:
        with transaction.atomic():
            project_items = instance.project_item_project.all()
            project_items.delete()

            #changing selected individual items to available if deleted
            try:
                individual_items_to_update = IndividualItem.objects.filter(
                    project_item_item_code__in=project_items
                )
                individual_items_to_update.update(is_available=True)
            except Exception as e:
                    raise Exception(f"Couldn't update availability after deletion of Project Item: {e}")
            print("below is_available=True")

    except Exception as e:
        raise Exception(f"Couldn't delete Project Items when deleting Project: {e}")