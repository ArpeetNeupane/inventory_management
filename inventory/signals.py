from django.db.models.signals import post_delete#, post_save
from django.dispatch import receiver
# from math import ceil
# from .models import Transaction, TransactionItem
from .models import Item

# ###here, instance is being used instead of self, as we're working with instance of Transcation and not of signal###
# @receiver(post_save, sender=Transaction)
# @receiver(post_delete, sender=TransactionItem)
# def update_transaction_prices(sender, instance, created, **kwargs):
#     transaction_instance = instance.transaction  #getting the associated Transaction
#     items = TransactionItem.objects.filter(transaction=transaction_instance)  #retrieving all related TransactionItems
#     total_price = sum(item.quantity * item.price for item in items)  #sum of quantity * price at once for all items
#     final_price_with_vat = ceil(1.13 * total_price)  #applying VAT (13%) and rounding up using ceil(ceiling)
    
#     #updating the Transaction object with the calculated values
#     transaction_instance.totalPrice = total_price
#     transaction_instance.finalPriceWithVat = final_price_with_vat
#     transaction_instance.save(update_fields=['totalPrice', 'finalPriceWithVat'])  #saving only the updated fields

# @receiver(post_delete, sender = Item)
# def delete_items(sender, instance, **kwargs):
#     instance.individual_items.all().delete() #using related name individual_items