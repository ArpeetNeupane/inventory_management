from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField
from inventory.models import *

class ItemSerializer(serializers.ModelSerializer):
    #used to include custom properties or computed fields in the serialized output
    available_quantity = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = ['id', 'itemName', 'itemQuantity', 'itemCategory', 'available_quantity']

    def get_available_quantity(self, obj):
        return obj.available_quantity

class IndividualItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndividualItem
        fields = ['id', 'item', 'itemCode', 'is_available']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'categoryName', 'categoryQuantity']

    def update(self, instance, validated_data):
        #checking if categoryQuantity is being updated
        if 'categoryQuantity' in validated_data:
            raise serializers.ValidationError("categoryQuantity cannot be updated this way.")
        
        #if categoryQuantity is not being updated, continue with the regular update
        return super().update(instance, validated_data)

class SupplierItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierItem
        fields = ['id', 'supplier', 'item', 'price', 'supply_date']

class SupplierSerializer(serializers.ModelSerializer):
    supplieritem_supplier = SupplierItemSerializer(many=True, read_only=True)

    class Meta:
        model = Supplier
        fields = ['id', 'supplierName', 'address', 'contactNo', 'supplieritem_supplier']

    #create method is used to customize how data is saved to the database when handling a POST request
    #need to override the create method to handle nested relationship such as supplieritem_supplier properly
    def create(self, validated_data):
        #extracting supplier items from validated data, using key supplieritem_supplier
        supplier_items_data = validated_data.pop('supplieritem_supplier', []) #[] --> default value if not found
        
        #creating the supplier instance
        supplier = Supplier.objects.create(**validated_data) #** used to unpack dict
        
        #creating SupplierItem instances for each entry in the supplieritem_supplier list
        for supplier_item_data in supplier_items_data:
            SupplierItem.objects.create(supplier=supplier, **supplier_item_data)
        
        return supplier

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


