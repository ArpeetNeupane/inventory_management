from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField
from inventory.models import *

class ItemSerializer(serializers.ModelSerializer):
    #used to include custom properties or computed fields in the serialized output
    available_quantity = SerializerMethodField()

    class Meta:
        model = Item
        fields = ['id', 'itemName', 'itemQuantity', 'itemCategory', 'available_quantity']

    def available_quantity(self, obj):
        return obj.available_quantity

class IndividualItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndividualItem
        fields = ['id', 'item', 'itemCode', 'is_available']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'categoryName', 'categoryQuantity']

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'supplierName', 'address', 'contactNo']

class SupplierItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierItem
        fields = ['id', 'supplier', 'item', 'price', 'supply_date']

class TransactionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionItem
        fields = ['id', 'transaction', 'item', 'quantity', 'price']

class TransactionSerializer(serializers.ModelSerializer):
    transactionitem_transaction = TransactionItemSerializer(many=True, read_only=True)

    class Meta:
        model = Transaction
        fields = ['id', 'billNo', 'supplier', 'totalPrice', 'finalPriceWithVat', 'date', 'paymentStatus', 'transactionitem_transaction']

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'projectName', 'projectLeader']


