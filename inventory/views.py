from django.shortcuts import get_object_or_404
from inventory_management.utils import api_response

from inventory.models import *
from inventory.serializers import *

from rest_framework import status
from rest_framework.views import APIView

#available q cant be greater than item exception
class ItemAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            items = Item.objects.all()
            item_serializer = ItemSerializer(items, many=True)
            return api_response(
                is_success=True,
                error_message=None,
                status_code=status.HTTP_200_OK,
                result = item_serializer.data,
            )
            
        except Item.DoesNotExist:
            return api_response(
                is_success=True,
                error_message="Item does not exist.",
                status_code=status.HTTP_404_NOT_FOUND,
                result = None,
            )
        
        except Exception as e:
            return api_response(
                is_success=False,
                error_message="An error occurred while fetching items. Please try again later." + str(e),
                status_code=status.HTTP_400_BAD_REQUEST,
                result=None,
            )

    def post(self, request, *args, **kwargs):
        try:
            new_item = request.data
            new_item_serializer = ItemSerializer(data=new_item)
            if new_item_serializer.is_valid():
                new_item_serializer.save()
                return api_response(
                    is_success=True,
                    error_message=None,
                    status_code=status.HTTP_201_CREATED,
                    result=new_item_serializer.data,
                )
            return api_response(
                is_success=False,
                error_message=new_item_serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
                result=None,
            )
        
        except Exception as e:
            return api_response(
                is_success=False,
                error_message=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                result=None,
            )
        
    def put(self, request, *args, **kwargs):
        try:
            item_id = request.data.get('id')

            if not item_id:
                return api_response(
                    is_success=False,
                    error_message="An ID must be provided to update an item.",
                    status_code=status.HTTP_400_BAD_REQUEST,
                    result=None,
                )
            
            existing_item = Item.objects.get(id=item_id)
            updated_item_serializer = ItemSerializer(instance=existing_item, data=request.data)
            if updated_item_serializer.is_valid():
                updated_item_serializer.save()
                return api_response(
                    is_success=True,
                    error_message=None,
                    status_code=status.HTTP_200_OK,
                    result=updated_item_serializer.data,
                )
            return api_response(
                    is_success=False,
                    error_message=updated_item_serializer.errors,
                    status_code=status.HTTP_400_BAD_REQUEST,
                    result=None,
                )

        except Item.DoesNotExist:
            return api_response(
                is_success=False,
                error_message="The item does not exist.",
                status_code=status.HTTP_404_NOT_FOUND,
                result=None,
            )
        
        except Exception as e:
            return api_response(
                is_success=False,
                error_message="An error occurred while updating the item. " + str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                result=None,
            )
        
    def delete(self, request, *args, **kwargs):
        try:
            item_id = request.data.get('id')

            if not item_id:
                return api_response(
                    is_success=False,
                    error_message="An ID must be provided to delete an item.",
                    status_code=status.HTTP_400_BAD_REQUEST,
                    result=None
                )
            
            deleted_item = Item.objects.get(id=item_id)
            deleted_item.delete()

            return api_response(
                is_success=True,
                error_message=None,
                status_code=status.HTTP_204_NO_CONTENT,
                result="Item deleted successfully.",
            )
        
        except Item.DoesNotExist:
            return api_response(
                is_success=False,
                error_message="The item does not exist.",
                status_code=status.HTTP_404_NOT_FOUND,
                result=None,
            )
        
        except Exception as e:
            return api_response(
                is_success=False,
                error_message="An error occurred while deleting the item. " + str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                result=None,
            )

class CategoryAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            categories = Category.objects.all()
            category_serializer = CategorySerializer(categories, many=True)
            return api_response(
                is_success=True,
                error_message=None,
                status_code=status.HTTP_200_OK,
                result=category_serializer.data,
            )
            
        except Category.DoesNotExist:
            return api_response(
                is_success=True,
                error_message="Category does not exist.",
                status_code=status.HTTP_404_NOT_FOUND,
                result = None,
            )
            
        except Exception as e:
            return api_response(
                is_success=False,
                error_message="An error occurred while fetching categories. Please try again later." + str(e),
                status_code=status.HTTP_400_BAD_REQUEST,
                result=None,
            )

    def post(self, request, *args, **kwargs):
        try:
            new_category = request.data
            new_category_serializer = CategorySerializer(data=new_category)
            if new_category_serializer.is_valid():
                new_category_serializer.save()
                return api_response(
                    is_success=True,
                    error_message=None,
                    status_code=status.HTTP_201_CREATED,
                    result=new_category_serializer.data,
                )
            return api_response(
                is_success=False,
                error_message=new_category_serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
                result=None,
            )
        
        except Exception as e:
            return api_response(
                is_success=False,
                error_message=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                result=None,
            )
        
    def put(self, request, *args, **kwargs):
        try:
            category_id = request.data.get('id')

            if not category_id:
                return api_response(
                    is_success=False,
                    error_message="An ID must be provided update a category.",
                    status_code=status.HTTP_400_BAD_REQUEST,
                    result=None,
                )
            
            existing_category = Category.objects.get(id=category_id)
            updated_category_serializer = CategorySerializer(instance=existing_category, data=request.data)
            if updated_category_serializer.is_valid():
                updated_category_serializer.save()
                return api_response(
                    is_success=True,
                    error_message=None,
                    status_code=status.HTTP_200_OK,
                    result=updated_category_serializer.data,
                )
            return api_response(
                    is_success=False,
                    error_message=updated_category_serializer.errors,
                    status_code=status.HTTP_400_BAD_REQUEST,
                    result=None,
                )

        except Category.DoesNotExist:
            return api_response(
                is_success=False,
                error_message="The category does not exist.",
                status_code=status.HTTP_404_NOT_FOUND,
                result=None,
            )
        
        except Exception as e:
            return api_response(
                is_success=False,
                error_message="An error occurred while updating the category. " + str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                result=None,
            )
        
    def delete(self, request, *args, **kwargs):
        try:
            category_id = request.data.get('id')

            if not category_id:
                return api_response(
                    is_success=False,
                    error_message="An ID must be provided to delete a category.",
                    status_code=status.HTTP_400_BAD_REQUEST,
                    result=None
                )
            
            deleted_category = Category.objects.get(id=category_id)
            deleted_category.delete()

            return api_response(
                is_success=True,
                error_message=None,
                status_code=status.HTTP_204_NO_CONTENT,
                result="Category deleted successfully.",
            )
        
        except Category.DoesNotExist:
            return api_response(
                is_success=False,
                error_message="The category does not exist.",
                status_code=status.HTTP_404_NOT_FOUND,
                result=None,
            )
        
        except Exception as e:
            return api_response(
                is_success=False,
                error_message="An error occurred while deleting the category. " + str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                result=None,
            )

class IndividualItemAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            individual_items = IndividualItem.objects.all()
            individual_item_serializer = IndividualItemSerializer(individual_items, many=True)
            return api_response(
                is_success=True,
                error_message=None,
                status_code=status.HTTP_200_OK,
                result = individual_item_serializer.data,
            )
            
        except IndividualItem.DoesNotExist:
            return api_response(
                is_success=False,
                error_message="The individual item does not exist.",
                status_code=status.HTTP_404_NOT_FOUND,
                result=None,
            )
        
        except Exception as e:
            return api_response(
                is_success=False,
                error_message="An error occurred while fetching individual item / item codes. Please try again later." + str(e),
                status_code=status.HTTP_400_BAD_REQUEST,
                result=None,
            )
        
    def delete(self, request, *args, **kwargs):
        try:
            individual_item_id = request.data.get('id')

            if not individual_item_id:
                return api_response(
                    is_success=False,
                    error_message="An ID must be provided to delete an individual item.",
                    status_code=status.HTTP_400_BAD_REQUEST,
                    result=None
                )
            
            deleted_individual_item = IndividualItem.objects.get(id=individual_item_id)
            deleted_individual_item.delete()

            return api_response(
                is_success=True,
                error_message=None,
                status_code=status.HTTP_204_NO_CONTENT,
                result="Individual item deleted successfully.",
            )
        
        except IndividualItem.DoesNotExist:
            return api_response(
                is_success=False,
                error_message="The individual item does not exist.",
                status_code=status.HTTP_404_NOT_FOUND,
                result=None,
            )
        
        except Exception as e:
            return api_response(
                is_success=False,
                error_message="An error occurred while deleting the individual item. " + str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                result=None,
            )

class SupplierAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            #fetching all suppliers, excluding their items
            suppliers = Supplier.objects.all()
            supplier_serializer = SupplierSerializer(suppliers, many=True)
            for supplier_data in supplier_serializer.data:
                supplier_data.pop('supplieritem_supplier', None)  #excluding items in list view

            return api_response(
                is_success=True,
                error_message=None,
                status_code=status.HTTP_200_OK,
                result=supplier_serializer.data,
            )

        except Exception as e:
            return api_response(
                is_success=False,
                error_message="An error occurred while fetching suppliers. " + str(e),
                status_code=status.HTTP_400_BAD_REQUEST,
                result=None,
            )

    def post(self, request, *args, **kwargs):
        try:
            new_supplier = request.data
            new_supplier_serializer = SupplierSerializer(data=new_supplier)
            if new_supplier_serializer.is_valid():
                new_supplier_serializer.save()
                return api_response(
                    is_success=True,
                    error_message=None,
                    status_code=status.HTTP_201_CREATED,
                    result=new_supplier_serializer.data,
                )
            return api_response(
                is_success=False,
                error_message=new_supplier_serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
                result=None,
            )
        
        except Exception as e:
            return api_response(
                is_success=False,
                error_message=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                result=None,
            )
        
    def put(self, request, *args, **kwargs):
        try:
            supplier_id = request.data.get('id')

            if not supplier_id:
                return api_response(
                    is_success=False,
                    error_message="Supplier ID is required.",
                    status_code=status.HTTP_400_BAD_REQUEST,
                    result=None,
                )
            
            existing_supplier = get_object_or_404(Supplier, id=supplier_id)
            updated_supplier_serializer = SupplierSerializer(instance=existing_supplier, data=request.data)
            if updated_supplier_serializer.is_valid():
                updated_supplier_serializer.save()
                return api_response(
                    is_success=True,
                    error_message=None,
                    status_code=status.HTTP_200_OK,
                    result=updated_supplier_serializer.data,
                )
            return api_response(
                    is_success=False,
                    error_message=updated_supplier_serializer.errors,
                    status_code=status.HTTP_400_BAD_REQUEST,
                    result=None,
                )

        except Supplier.DoesNotExist:
            return api_response(
                is_success=False,
                error_message="The supplier does not exist.",
                status_code=status.HTTP_404_NOT_FOUND,
                result=None,
            )
        
        except Exception as e:
            return api_response(
                is_success=False,
                error_message="An error occurred while updating the supplier. " + str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                result=None,
            )
        
    def delete(self, request, *args, **kwargs):
        try:
            supplier_id = request.data.get('id')

            if not supplier_id:
                return api_response(
                    is_success=False,
                    error_message="An ID must be provided to delete a supplier.",
                    status_code=status.HTTP_400_BAD_REQUEST,
                    result=None
                )
            
            deleted_supplier = Supplier.objects.get(id=supplier_id)
            deleted_supplier.delete()

            return api_response(
                is_success=True,
                error_message=None,
                status_code=status.HTTP_204_NO_CONTENT,
                result="Supplier deleted successfully.",
            )
        
        except Supplier.DoesNotExist:
            return api_response(
                is_success=False,
                error_message="The supplier does not exist.",
                status_code=status.HTTP_404_NOT_FOUND,
                result=None,
            )
        
        except Exception as e:
            return api_response(
                is_success=False,
                error_message="An error occurred while deleting the supplier. " + str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                result=None,
            )

class SupplierItemAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            supplier_id = kwargs.get('id')  #getting supplier ID from the URL if provided

            if not supplier_id:
                return api_response(
                    is_success=False,
                    error_message="An ID must be provided in the url to view supplier items.",
                    status_code=status.HTTP_400_BAD_REQUEST,
                    result=None
                )

            #fetching the specific supplier items excluding supplier details
            supplier = get_object_or_404(Supplier, id=supplier_id)
            supplier_item = supplier.supplieritem_supplier.all()
            supplier_item_serializer = SupplierItemSerializer(supplier_item, many=True)

            return api_response(
                is_success=True,
                error_message=None,
                status_code=status.HTTP_200_OK,
                result=supplier_item_serializer.data,
            )

        except Exception as e:
            return api_response(
                is_success=False,
                error_message="An error occurred while fetching supplier items. " + str(e),
                status_code=status.HTTP_400_BAD_REQUEST,
                result=None,
            )

    def post(self, request, *args, **kwargs):
        try:
            supplier_id = request.data

            supplier_foreign_key = request.data.get('supplier')
            if int(supplier_foreign_key) != int(supplier_id):
                raise Exception("Supplier Mismatch")

            new_supplier_item = request.data
            new_supplier_item_serializer = SupplierItemSerializer(data=new_supplier_item)
            if new_supplier_item_serializer.is_valid():
                new_supplier_item_serializer.save()
                return api_response(
                    is_success=True,
                    error_message=None,
                    status_code=status.HTTP_201_CREATED,
                    result=new_supplier_item_serializer.data,
                )
            return api_response(
                is_success=False,
                error_message=new_supplier_item_serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
                result=None,
            )
        
        except Exception as e:
            return api_response(
                is_success=False,
                error_message=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                result=None,
            )
        
    def put(self, request, *args, **kwargs):
        try:
            supplier_item_id = request.data.get('id')

            if not supplier_item_id:
                return api_response(
                    is_success=False,
                    error_message="Supplier item id is required.",
                    status_code=status.HTTP_400_BAD_REQUEST,
                    result=None,
                )
            
            existing_supplier_item = get_object_or_404(SupplierItem, id=supplier_item_id)
            updated_supplier_item_serializer = SupplierItemSerializer(instance=existing_supplier_item, data=request.data)
            if updated_supplier_item_serializer.is_valid():
                updated_supplier_item_serializer.save()
                return api_response(
                    is_success=True,
                    error_message=None,
                    status_code=status.HTTP_200_OK,
                    result=updated_supplier_item_serializer.data,
                )
            return api_response(
                    is_success=False,
                    error_message=updated_supplier_item_serializer.errors,
                    status_code=status.HTTP_400_BAD_REQUEST,
                    result=None,
                )

        except SupplierItem.DoesNotExist:
            return api_response(
                is_success=False,
                error_message="The supplier item does not exist.",
                status_code=status.HTTP_404_NOT_FOUND,
                result=None,
            )
        
        except Exception as e:
            return api_response(
                is_success=False,
                error_message="An error occurred while updating the supplier item. " + str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                result=None,
            )
        
    def delete(self, request, *args, **kwargs):
        try:
            supplier_item_id = request.data.get('id')

            if not supplier_item_id:
                return api_response(
                    is_success=False,
                    error_message="An ID must be provided to delete a supplier.",
                    status_code=status.HTTP_400_BAD_REQUEST,
                    result=None
                )
            
            deleted_supplier_item = SupplierItem.objects.get(id=supplier_item_id)
            deleted_supplier_item.delete()

            return api_response(
                is_success=True,
                error_message=None,
                status_code=status.HTTP_204_NO_CONTENT,
                result="Supplier item deleted successfully.",
            )
        
        except SupplierItem.DoesNotExist:
            return api_response(
                is_success=False,
                error_message="The supplier item does not exist.",
                status_code=status.HTTP_404_NOT_FOUND,
                result=None,
            )
        
        except Exception as e:
            return api_response(
                is_success=False,
                error_message="An error occurred while deleting the supplier item. " + str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                result=None,
            )

class PurchaseAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            #fetching all purchase, excluding their items
            purchase = Purchase.objects.all()
            purchase_serializer = PurchaseSerializer(purchase, many=True)
            for supplier_data in purchase_serializer.data:
                supplier_data.pop('purchaseitem_purchase', None)  #excluding items in list view

            return api_response(
                is_success=True,
                error_message=None,
                status_code=status.HTTP_200_OK,
                result=purchase_serializer.data,
            )
            
        except Purchase.DoesNotExist:
            return api_response(
                is_success=False,
                error_message="The purchase does not exist.",
                status_code=status.HTTP_404_NOT_FOUND,
                result=None,
            )
        
        except Exception as e:
            return api_response(
                is_success=False,
                error_message="An error occurred while fetching purchases. Please try again later." + str(e),
                status_code=status.HTTP_400_BAD_REQUEST,
                result=None,
            )

    def post(self, request, *args, **kwargs):
        try:
            new_purchase = request.data
            new_purchase_serializer = PurchaseSerializer(data=new_purchase)
            if new_purchase_serializer.is_valid():
                new_purchase_serializer.save()
                return api_response(
                    is_success=True,
                    error_message=None,
                    status_code=status.HTTP_201_CREATED,
                    result=new_purchase_serializer.data,
                )
            return api_response(
                is_success=False,
                error_message=new_purchase_serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
                result=None,
            )
        
        except Exception as e:
            return api_response(
                is_success=False,
                error_message=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                result=None,
            )
        
    def put(self, request, *args, **kwargs):
        try:
            purchase_id = request.data.get('id')

            if not purchase_id:
                return api_response(
                    is_success=False,
                    error_message="An ID must be provided to update a purchase.",
                    status_code=status.HTTP_400_BAD_REQUEST,
                    result=None,
                )
            
            existing_purchase = Purchase.objects.get(id=purchase_id)
            updated_purchase_serializer = PurchaseSerializer(instance=existing_purchase, data=request.data)
            if updated_purchase_serializer.is_valid():
                updated_purchase_serializer.save()
                return api_response(
                    is_success=True,
                    error_message=None,
                    status_code=status.HTTP_200_OK,
                    result=updated_purchase_serializer.data,
                )
            return api_response(
                    is_success=False,
                    error_message=updated_purchase_serializer.errors,
                    status_code=status.HTTP_400_BAD_REQUEST,
                    result=None,
                )

        except Purchase.DoesNotExist:
            return api_response(
                is_success=False,
                error_message="The purchase does not exist.",
                status_code=status.HTTP_404_NOT_FOUND,
                result=None,
            )
        
        except Exception as e:
            return api_response(
                is_success=False,
                error_message="An error occurred while updating the purchase. " + str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                result=None,
            )
        
    def delete(self, request, *args, **kwargs):
        try:
            #getting purchase id
            purchase_id = request.data.get('id')

            if not purchase_id:
                return api_response(
                    is_success=False,
                    error_message="An ID must be provided in the url to delete a purchase.",
                    status_code=status.HTTP_400_BAD_REQUEST,
                    result=None
                )
            
            deleted_purchase = Purchase.objects.get(id=purchase_id)
            deleted_purchase.delete()

            return api_response(
                is_success=True,
                error_message=None,
                status_code=status.HTTP_204_NO_CONTENT,
                result="Purchase deleted successfully.",
            )
        
        except Purchase.DoesNotExist:
            return api_response(
                is_success=False,
                error_message="The purchase does not exist.",
                status_code=status.HTTP_404_NOT_FOUND,
                result=None,
            )
        
        except Exception as e:
            return api_response(
                is_success=False,
                error_message="An error occurred while deleting the purchase. " + str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                result=None,
            )
        
class PurchaseItemAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            purchase_id = kwargs.get('id') #getting purchase ID from the URL if provided

            if not purchase_id:
                return api_response(
                    is_success=False,
                    error_message="An ID must be provided in the url to view purchase items.",
                    status_code=status.HTTP_400_BAD_REQUEST,
                    result=None
                )

            #fetching the specific purchase items excluding supplier details
            purchase = get_object_or_404(Purchase, id=purchase_id)
            purchase_item = purchase.purchaseitem_purchase.all()
            purchase_item_serializer = PurchaseItemSerializer(purchase_item, many=True)

            return api_response(
                is_success=True,
                error_message=None,
                status_code=status.HTTP_200_OK,
                result=purchase_item_serializer.data,
            )
            
        except PurchaseItem.DoesNotExist:
            return api_response(
                is_success=False,
                error_message="The purchase item does not exist.",
                status_code=status.HTTP_404_NOT_FOUND,
                result=None,
            )
        
        except Exception as e:
            return api_response(
                is_success=False,
                error_message="An error occurred while fetching purchase items. Please try again later." + str(e),
                status_code=status.HTTP_400_BAD_REQUEST,
                result=None,
            )

    def post(self, request, *args, **kwargs):
        try:
            new_purchase_item = request.data
            new_purchase_item_serializer = PurchaseItemSerializer(data=new_purchase_item)
            if new_purchase_item_serializer.is_valid():
                new_purchase_item_serializer.save()
                return api_response(
                    is_success=True,
                    error_message=None,
                    status_code=status.HTTP_201_CREATED,
                    result=new_purchase_item_serializer.data,
                )
            return api_response(
                is_success=False,
                error_message=new_purchase_item_serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
                result=None,
            )
        
        except Exception as e:
            return api_response(
                is_success=False,
                error_message=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                result=None,
            )
        
    def put(self, request, *args, **kwargs):
        try:
            purchase_item_id = request.data.get("id")

            if not purchase_item_id:
                return api_response(
                    is_success=False,
                    error_message="An ID must be provided to update a purchase item.",
                    status_code=status.HTTP_400_BAD_REQUEST,
                    result=None,
                )
            
            existing_purchase_item = PurchaseItem.objects.get(id=purchase_item_id)
            updated_purchase_item_serializer = PurchaseItemSerializer(instance=existing_purchase_item, data=request.data)
            if updated_purchase_item_serializer.is_valid():
                updated_purchase_item_serializer.save()
                return api_response(
                    is_success=True,
                    error_message=None,
                    status_code=status.HTTP_200_OK,
                    result=updated_purchase_item_serializer.data,
                )
            return api_response(
                    is_success=False,
                    error_message=updated_purchase_item_serializer.errors,
                    status_code=status.HTTP_400_BAD_REQUEST,
                    result=None,
                )

        except PurchaseItem.DoesNotExist:
            return api_response(
                is_success=False,
                error_message="The purchase item does not exist.",
                status_code=status.HTTP_404_NOT_FOUND,
                result=None,
            )
        
        except Exception as e:
            return api_response(
                is_success=False,
                error_message="An error occurred while updating purchase item. " + str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                result=None,
            )
        
    def delete(self, request, *args, **kwargs):
        try:
            purchase_item_id = request.data.get('id')

            if not purchase_item_id:
                return api_response(
                    is_success=False,
                    error_message="An ID must be provided to delete a purchase item.",
                    status_code=status.HTTP_400_BAD_REQUEST,
                    result=None
                )
            
            deleted_purchase = PurchaseItem.objects.get(id=purchase_item_id)
            deleted_purchase.delete()

            return api_response(
                is_success=True,
                error_message=None,
                status_code=status.HTTP_204_NO_CONTENT,
                result="Purchase Item deleted successfully.",
            )
        
        except PurchaseItem.DoesNotExist:
            return api_response(
                is_success=False,
                error_message="The purchase item does not exist.",
                status_code=status.HTTP_404_NOT_FOUND,
                result=None,
            )
        
        except Exception as e:
            return api_response(
                is_success=False,
                error_message="An error occurred while deleting the purchase item. " + str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                result=None,
            )

class ProjectAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            #fetching all projects, excluding their items
            projects = Project.objects.all()
            project_serializer = ProjectSerializer(projects, many=True)
            for supplier_data in project_serializer.data:
                supplier_data.pop('project_item_project', None)  #excluding items in list view

            return api_response(
                is_success=True,
                error_message=None,
                status_code=status.HTTP_200_OK,
                result=project_serializer.data,
            )

        except Exception as e:
            return api_response(
                is_success=False,
                error_message="The project does not exist",
                status_code=status.HTTP_400_BAD_REQUEST,
                result=None,
            )
        
    def post(self, request, *args, **kwargs):
        try:
            new_project = request.data
            new_project_serializer = ProjectSerializer(data=new_project)
            if new_project_serializer.is_valid():
                new_project_serializer.save()
                return api_response(
                    is_success=True,
                    error_message=None,
                    status_code=status.HTTP_201_CREATED,
                    result=new_project_serializer.data,
                )
            return api_response(
                is_success=True,
                error_message=new_project_serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
                result=None,
            )

        except Exception as e:
            return api_response(
                is_success=False,
                error_message=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                result=None,
            )
        
    def put(self, request, *args, **kwargs):
        try:
            project_id = request.data.get('id')
            if not project_id:
                return api_response(
                    is_success=False,
                    error_message="An ID must be provided to update a project.",
                    status_code=status.HTTP_400_BAD_REQUEST,
                    result=None,
                )
            
            existing_project = Project.objects.get(id=project_id)
            updated_project_serializer = ProjectSerializer(instance=existing_project, data=request.data)
            if updated_project_serializer.is_valid():
                updated_project_serializer.save()
                return api_response(
                    is_success=True,
                    error_message=None,
                    status_code=status.HTTP_200_OK,
                    result=updated_project_serializer.data,
                )
            return api_response(
                    is_success=False,
                    error_message=updated_project_serializer.errors,
                    status_code=status.HTTP_400_BAD_REQUEST,
                    result=None,
                )

        except Project.DoesNotExist:
            return api_response(
                is_success=False,
                error_message="The project does not exist.",
                status_code=status.HTTP_404_NOT_FOUND,
                result=None,
            )
        
        except Exception as e:
            return api_response(
                is_success=False,
                error_message="An error occurred while updating the project. " + str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                result=None,
            )

    def delete(self, request, *args, **kwargs):
        try:
            project_id = request.data.get('id')

            if not project_id:
                return api_response(
                is_success=False,
                error_message="An ID must be provided to delete a project.",
                status_code=status.HTTP_404_NOT_FOUND,
                result=None,
            )

            deleted_project = Project.objects.get(id=project_id)
            deleted_project.delete()

            return api_response(
                is_success=True,
                error_message=None,
                status_code=status.HTTP_204_NO_CONTENT,
                result="Project deleted successfully.",
            )

        except Project.DoesNotExist:
            return api_response(
                is_success=False,
                error_message="The project does not exist.",
                status_code=status.HTTP_404_NOT_FOUND,
                result=None,
            )
        
        except Exception as e:
            return api_response(
                is_success=False,
                error_message="An error occurred while deleting the project. " + str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                result=None,
            )
        
class ProjectItemAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            project_item_id = kwargs.get('id')  #getting project ID from the URL if provided

            if not project_item_id:
                return api_response(
                    is_success=False,
                    error_message="An ID must be provided in the url to view project items.",
                    status_code=status.HTTP_400_BAD_REQUEST,
                    result=None
                )

            #fetching the specific project items excluding project details
            project = get_object_or_404(Project, id=project_item_id)
            project_item = project.project_item_project.all()
            project_item_serializer = ProjectItemSerializer(project_item, many=True)

            return api_response(
                is_success=True,
                error_message=None,
                status_code=status.HTTP_200_OK,
                result=project_item_serializer.data,
            )

        except Exception as e:
            return api_response(
                is_success=False,
                error_message="The project item does not exist",
                status_code=status.HTTP_400_BAD_REQUEST,
                result=None,
            )
        
    def post(self, request, *args, **kwargs):
        try:
            new_project_item = request.data
            new_project_item_serializer = ProjectItemSerializer(data=new_project_item)
            if new_project_item_serializer.is_valid():
                new_project_item_serializer.save()
                return api_response(
                    is_success=True,
                    error_message=None,
                    status_code=status.HTTP_201_CREATED,
                    result=new_project_item_serializer.data,
                )
            return api_response(
                is_success=True,
                error_message=new_project_item_serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
                result=None,
            )

        except Exception as e:
            return api_response(
                is_success=False,
                error_message=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                result=None,
            )
        
    def put(self, request, *args, **kwargs):
        try:
            project_item_id = request.data.get('id')
            if not project_item_id:
                return api_response(
                    is_success=False,
                    error_message="An ID must be provided to update a project item.",
                    status_code=status.HTTP_400_BAD_REQUEST,
                    result=None,
                )
            
            existing_project_item = ProjectItem.objects.get(id=project_item_id)
            updated_project_item_serializer = ProjectItemSerializer(instance=existing_project_item, data=request.data)
            if updated_project_item_serializer.is_valid():
                updated_project_item_serializer.save()
                return api_response(
                    is_success=True,
                    error_message=None,
                    status_code=status.HTTP_200_OK,
                    result=updated_project_item_serializer.data,
                )
            return api_response(
                    is_success=False,
                    error_message=updated_project_item_serializer.errors,
                    status_code=status.HTTP_400_BAD_REQUEST,
                    result=None,
                )

        except ProjectItem.DoesNotExist:
            return api_response(
                is_success=False,
                error_message="The project item does not exist.",
                status_code=status.HTTP_404_NOT_FOUND,
                result=None,
            )
        
        except Exception as e:
            return api_response(
                is_success=False,
                error_message="An error occurred while updating the project item. " + str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                result=None,
            )

    def delete(self, request, *args, **kwargs):
        try:
            project_item_id = request.data.get('id')

            if not project_item_id:
                return api_response(
                is_success=False,
                error_message="An ID must be provided to delete a project item.",
                status_code=status.HTTP_404_NOT_FOUND,
                result=None,
            )

            deleted_project = ProjectItem.objects.get(id=project_item_id)
            deleted_project.delete()

            return api_response(
                is_success=True,
                error_message=None,
                status_code=status.HTTP_204_NO_CONTENT,
                result="Project item deleted successfully.",
            )

        except ProjectItem.DoesNotExist:
            return api_response(
                is_success=False,
                error_message="The project item does not exist.",
                status_code=status.HTTP_404_NOT_FOUND,
                result=None,
            )
        
        except Exception as e:
            return api_response(
                is_success=False,
                error_message="An error occurred while deleting the project. " + str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                result=None,
            )