from django.db import models

class Items(models.Model):
    item_name = models.CharField(max_length=23)
    quantity = models.PositiveIntegerField()
    category = models.CharField(max_length=29)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    bill_no = models.CharField(max_length=10)
    supplier = models.CharField(max_length=50)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.item_name
    
class Categories(models.Model):
    category_name = models.CharField(max_length=23)
    no_of_items_in_category = models.PositiveIntegerField()

    def __str__(self):
        return self.category_name


