from django.db import transaction
# from django.db import connection
from django.db.models.signals import post_delete, post_save, pre_save, pre_delete, m2m_changed
from django.db.models import Sum, F
from django.db.utils import DatabaseError, IntegrityError
from django.dispatch import receiver
from math import ceil
from inventory.models import *
from django.core.exceptions import ValidationError
# from inventory_management.utils import api_response

###################
###what what items in a category
#a item sold by what what suppliers
#item doesnot exist exception
#views change garnu parne xa
#json ma item lai name le represent garne instead of pk
###################

#capturing old quantity of PurchaseItem
@receiver(pre_save, sender=PurchaseItem)
def capture_original_quantities(sender, instance, **kwargs):
    #checking if old or new instances, only doing this for existing instances
    if instance.pk:
        try:
            #storing original quantities for all items in purchase_items, filter: items filtered are of the same purchase as as purchase of current instance
            purchase_items = PurchaseItem.objects.filter(purchase=instance.purchase)
            
            #dictionary to store original quantities
            original_quantities = {}
            for trans_item in purchase_items:
                #storing quantity of current PurchaseItem
                original_quantities[trans_item.pk] = trans_item.quantity
            
            #attaching to the instance as a temporary attribute
            instance._original_quantities = original_quantities
        except Exception as e:
            instance._original_quantities = {}


###here, instance is being used instead of self, as we're working with instance of Transcation and not of signal###
@receiver([post_save, post_delete], sender=PurchaseItem)
def update_purchase(sender, instance, created=None, **kwargs):
    try:
        with transaction.atomic(): #ensuring atomicity(so that all calculations are implemented at once and if error occurs, it's rolled back)
            if hasattr(instance, 'purchase') and instance.purchase:
                #first checking if the instance has attribute purchase, and secondly checking if the instance has a truthy value(meaning value exists and is not false, null, 0 or an empty string)
                #hasattr is redundant remove later
                purchase_instance = instance.purchase

                ####This is another approach but has a bottleneck for large datasets; memory inefficient####
                # related_items = PurchaseItem.objects.filter(purchase=purchase_instance) #retreiving items that belong to current instance and is PurchaseItems' object
                # #keyword argument for filter is name of model field(in this case is the foreign key field) and value is value you're filtering by
                # if related_items.exists():
                #     #checking if any items exists in current instance
                #     totalPrice = sum(item.quantity * item.price for item in related_items)
                #     finalPriceWithVat = ceil(totalPrice * 1.13)
                # else:
                #     #if not, by default, 0
                #     totalPrice = 0
                #     finalPriceWithVat = 0

                #retreiving items that belong to current instance and is PurchaseItems' object
                #aggregating the total price directly in the database
                result = PurchaseItem.objects.filter(purchase=purchase_instance).aggregate(
                    total_price=Sum(F('quantity') * F('price')) #F allows you to reference model field values directly in database queries
                    #aggregate --> basically means that the multiplication happens efficiently at the database level, avoiding the need to load the entire dataset into memory and perform the operation in Python
                )
                
                #extracting the total price from the result dictionary (defaulting to 0 if there's no result)
                totalPrice = result['total_price'] or 0
                
                # Calculate the final price with VAT
                finalPriceWithVat = ceil(totalPrice * 1.13)

                purchase_instance.totalPrice = totalPrice
                purchase_instance.finalPriceWithVat = finalPriceWithVat
                purchase_instance.save(update_fields=['totalPrice', 'finalPriceWithVat'])

    except DatabaseError as db_error:
        raise Exception(f"Error while updating purchase: {str(db_error)}")
    except Exception as e:
        print(f"Unexpected error: {e}")

    try:
        with transaction.atomic():
            purchase_items = PurchaseItem.objects.filter(purchase=instance.purchase)

            if kwargs.get('signal') == post_save:   
                if created:  #if the PurchaseItem is newly created, adding the quantity to the Item
                    print("Newly Created!")

                    #updating quantity
                    instance.item.itemQuantity += instance.quantity
                    instance.item.save()

                    #updating prices according to inputted price during PurchaseItem creation
                    #filtering all individual items for this item, which matches the instance and is_available
                    individual_items = IndividualItem.objects.filter(
                        item=instance.item, 
                        is_available=True
                    ).order_by('itemCode')[:instance.quantity] #slicing to only the number of quantity the same as when creating PurchaseItem so as to not overload
                    
                    #updating prices for these individual items
                    try:
                        for ind_item in individual_items:
                            ind_item.price = instance.price
                            ind_item.save(update_fields=['price'])
                    
                    except Exception as e:
                        print(f"Error updating individual item prices: {e}")

                else:  #if the PurchaseItem is updated, getting the previous quantity before updating
                    print("Not Newly Created but updated!")
                    #first, getting original quantity from pre_save
                    original_quantities = getattr(instance, '_original_quantities', {}) #default is {} if no value

                    for trans_item in purchase_items:
                    #if item is being updated, calculate quantity difference
                        if trans_item.pk == instance.pk:
                            original_quantity = original_quantities.get(trans_item.pk, trans_item.quantity)
                            #get(trans_item.pk, trans_item.quantity) 
                            quantity_diff = instance.quantity - original_quantity
                            
                            #updating quantity
                            trans_item.item.itemQuantity += quantity_diff
                            trans_item.item.save()

                            #updating prices according to inputted price during PurchaseItem creation
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
                #subtracting the quantity if a PurchaseItem is deleted
                    
                instance.item.itemQuantity -= instance.quantity
                instance.item.save()
                
    except Exception as e:
        raise Exception(f"Error while updating item quantity from purchase item: {e}")


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

        
@receiver(pre_delete, sender=Purchase)
def update_purchase_on_purchaseitem_delete(sender, instance, **kwargs):
    try:
        items_in_deleted_purchase = PurchaseItem.objects.filter(purchase=instance) #here, purchase=instance and not purchase=instance.purchase as the sender is purchase itself and it most likely doesn't have field referring to itself (unless there is)
        
        for item_in_deleted_purchase in items_in_deleted_purchase:
            quantity_of_deleted_item = item_in_deleted_purchase.quantity
            print(quantity_of_deleted_item)
            #*****if in future, manually handling itemQuantity after deletion of purchase is needed, code here*******

    except Exception as e:
        raise Exception(f"Couldn't calculate changes in item quantity after deletion of purchase: {e}")


@receiver(post_delete, sender=Purchase)
def delete_purchaseitems_when_purchase_delete(sender, instance, **kwargs):
    try:
        with transaction.atomic():
            instance.purchaseitem_purchase.all().delete()

    except Exception as e:
        raise Exception(f"Couldn't delete Purchase Items when deleting Transacation: {e}")


@receiver(pre_save, sender=SupplierItem)
def validate_supplier_item(sender, instance, **kwargs):
    #checking if this supplier already has this item
    existing_item = SupplierItem.objects.filter(
        supplier=instance.supplier,
        item=instance.item
    ).exclude(pk=instance.pk).first()

    if existing_item:
        raise ValidationError(f"Supplier {instance.supplier.supplierName} already sells {instance.item.itemName}.")

    
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
                    raise Exception(f"Couldn't update availability after deletion of Project Item from Project: {e}")
            print("below is_available=True")

    except Exception as e:
        raise Exception(f"Couldn't delete Project Items when deleting Project: {e}")


@receiver(pre_delete, sender=ProjectItem)
def handle_deletion_of_projectitems(sender, instance, **kwargs):
    try:
        with transaction.atomic():
            print("inside post_delete of projectitem")

            individual_items = instance.individual_items.all()
            if individual_items.exists():
                print(f"Individual items related: {individual_items}")
                for item in individual_items:
                    item.is_available = True
                    item.save()  # This saves the item with availability set to True
                    print(f"Item {item.itemCode} set to available.")
            else:
                print("No individual items found.")
    except Exception as e:
        print(f"Error in post_delete signal: {e}")
        raise Exception(f"Couldn't change availability after deletion of Project Item: {e}")


@receiver(pre_save, sender=ProjectItem)
def validate_item_availability(sender, instance, *args, **kwargs):
    #skipping validation if its is a deletion
    if instance.quantity == 0:
        return
        
    with transaction.atomic():
        #getting currently assigned items for existing instances
        currently_assigned = set()
        if instance.pk:
            currently_assigned = set(
                instance.individual_items.values_list('id', flat=True)
            )
            
        #calculating how many additional items we need
        available_items = instance.item.individual_items.filter(
            is_available=True
        ).exclude(
            id__in=currently_assigned
        )
        available_count = available_items.count()
        
        #for updates, we need to check if we're increasing or decreasing quantity
        if instance.pk:
            original = ProjectItem.objects.get(pk=instance.pk)
            additional_needed = instance.quantity - original.quantity
        else:
            additional_needed = instance.quantity
            
        if additional_needed > available_count:
            curr_total = available_count + len(currently_assigned)
            raise ValidationError(
                f'Not enough available items. Requested: {instance.quantity}, '
                f'Currently assigned: {len(currently_assigned)}, '
                f'Additional available: {available_count}, '
                f'Total available: {curr_total}'
            )


@receiver(post_save, sender=ProjectItem)
def manage_individual_items(sender, instance, created, **kwargs):
    with transaction.atomic():
        if created:
            #handling newly created ProjectItems
            assign_new_items(instance)
        else:
            #handling updated ProjectItems
            update_assigned_items(instance)


def assign_new_items(instance):
    available_items = instance.item.individual_items.filter(
        is_available=True
    ).order_by('itemCode')[:instance.quantity]
    
    for item in available_items:
        item.is_available = False
        item.save()
        instance.individual_items.add(item)


def update_assigned_items(instance):
    current_count = instance.individual_items.count()
    
    if instance.quantity > current_count:
        #if needed to add more items
        additional_needed = instance.quantity - current_count
        new_items = instance.item.individual_items.filter(
            is_available=True
        ).order_by('itemCode')[:additional_needed]
        
        for item in new_items:
            item.is_available = False
            item.save()
            instance.individual_items.add(item)
            
    elif instance.quantity < current_count:
        #if needed to remove some items
        items_to_remove = instance.individual_items.order_by('-itemCode')[:current_count - instance.quantity]
        
        for item in items_to_remove:
            item.is_available = True
            item.save()
            instance.individual_items.remove(item)


#