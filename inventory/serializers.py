from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField
from rest_framework.exceptions import ValidationError
from inventory.models import *
from django.shortcuts import get_object_or_404

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
        fields = ['id', 'supplier', 'item', 'price']
        read_only_fields = ['id'] #preventing accidental updates to these fields

class SupplierSerializer(serializers.ModelSerializer):
    supplieritem_supplier = SupplierItemSerializer(many=True, required=False)

    class Meta:
        model = Supplier
        fields = ['id', 'supplierName', 'address', 'contactNo', 'supplieritem_supplier']

    def create(self, validated_data):
        supplier_items_data = validated_data.pop('supplieritem_supplier', []) #removing supplieritem_supplier from data validated through serialization and retrieving it
        supplier = Supplier.objects.create(**validated_data) #creating a new supplier instance from remaining validated_data
        #(**) unpacks the dictionary, passing its keys and values as keyword arguments

        #creating SupplierItem instances only if supplier_items_data is not empty
        for supplier_item_data in supplier_items_data:
            SupplierItem.objects.create(supplier=supplier, **supplier_item_data) #supplier=supplier associating supplier item with previouly created supplier

        return supplier
    
    def update(self, instance, validated_data):
        # Update supplier fields
        instance.supplierName = validated_data.get('supplierName', instance.supplierName)
        instance.address = validated_data.get('address', instance.address)
        instance.contactNo = validated_data.get('contactNo', instance.contactNo)
        instance.save()

        # Handle nested supplier items
        supplier_items_data = validated_data.pop('supplieritem_supplier', [])
        existing_items = {item.id: item for item in instance.supplieritem_supplier.all()}

        for item_data in supplier_items_data:
            item_id = item_data.get('id')  # DRF ensures IDs are integers
            if item_id and item_id in existing_items:
                # Update existing SupplierItem
                supplier_item = existing_items.pop(item_id)
                for attr, value in item_data.items():
                    if attr != 'id':  # Skip ID field
                        setattr(supplier_item, attr, value)
                supplier_item.save()
            elif not item_data.get('id'):  # If no ID, treat as new
                item_data['supplier'] = instance
                SupplierItem.objects.create(**item_data)

        return instance

class TransactionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionItem
        fields = ['id', 'transaction', 'category', 'item', 'quantity', 'price']

class TransactionSerializer(serializers.ModelSerializer):
    transactionitem_transaction = TransactionItemSerializer(many=True, read_only=True)

    class Meta:
        model = Transaction
        fields = ['id', 'billNo', 'supplier', 'totalPrice', 'finalPriceWithVat', 'paymentStatus', 'transactionitem_transaction']

class ProjectItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectItem
        fields = ['id', 'associated_project', 'item', 'quantity', 'individual_items']

class ProjectSerializer(serializers.ModelSerializer):
    project_item_project = ProjectItemSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'projectName', 'projectLeader', 'project_item_project']


