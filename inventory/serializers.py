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

class SupplierItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierItem
        fields = ['id', 'supplier', 'item', 'price', 'supply_date']

class SupplierSerializer(serializers.ModelSerializer):
    supplieritem_supplier = SupplierItemSerializer(many=True, read_only=True)

    class Meta:
        model = Supplier
        fields = ['id', 'supplierName', 'address', 'contactNo', 'supplieritem_supplier']

class TransactionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionItem
        fields = ['id', 'transaction', 'item', 'quantity', 'price']

class TransactionSerializer(serializers.ModelSerializer):
    transactionitem_transaction = TransactionItemSerializer(many=True, read_only=True)

    class Meta:
        model = Transaction
        fields = ['id', 'billNo', 'supplier', 'totalPrice', 'finalPriceWithVat', 'date', 'paymentStatus', 'transactionitem_transaction']

class ProjectItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectItem
        fields = ['id', 'associated_project', 'item', 'quantity', 'start_date', 'individual_items']

class ProjectSerializer(serializers.ModelSerializer):
    project_item_project = ProjectItemSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'projectName', 'projectLeader', 'project_item_project']


