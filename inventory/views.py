from django.shortcuts import HttpResponse
from inventory_management.utils import api_response

from inventory.models import Item, Category, IndividualItem, Supplier, Transaction, Project
from inventory.serializers import ItemSerializer, CategorySerializer, IndividualItemSerializer, SupplierSerializer, TransactionSerializer, ProjectSerializer

from rest_framework import status
from rest_framework.views import APIView

class ItemAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            if 'id' in kwargs:
                item = Item.objects.get(id=kwargs['id'])
                item_serializer = ItemSerializer(item)
                return api_response(
                    is_success=True,
                    error_message=None,
                    status_code=status.HTTP_200_OK,
                    result = item_serializer.data,
                )

            else:
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
            #getting id from url
            item_id = kwargs.get('id')

            if not item_id:
                return api_response(
                    is_success=False,
                    error_message="An ID must be provided in the URL to update an item.",
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
            #getting item id from url
            item_id = kwargs.get('id')

            if not item_id:
                return api_response(
                    is_success=False,
                    error_message="An ID must be provided in the url to delete an item.",
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
            if 'id' in kwargs:
                category = Category.objects.get(id=kwargs['id'])
                category_serializer = CategorySerializer(category)
                return api_response(
                    is_success=True,
                    error_message=None,
                    status_code=status.HTTP_200_OK,
                    result=category_serializer.data,
                )
                
            else:
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
            #getting id from url
            category_id = kwargs.get('id')

            if not category_id:
                return api_response(
                    is_success=False,
                    error_message="An ID must be provided in the URL to update a category.",
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
            #getting category id from url
            category_id = kwargs.get('id')

            if not category_id:
                return api_response(
                    is_success=False,
                    error_message="An ID must be provided in the url to delete a category.",
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
            if 'id' in kwargs:
                individual_item = IndividualItem.objects.get(id=kwargs['id'])
                individual_item_serializer = IndividualItemSerializer(individual_item)
                return api_response(
                    is_success=True,
                    error_message=None,
                    status_code=status.HTTP_200_OK,
                    result = individual_item_serializer.data,
                )
            else:
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

    def post(self, request, *args, **kwargs):
        try:
            new_individual_item = request.data
            new_individual_item_serializer = IndividualItemSerializer(data=new_individual_item)
            if new_individual_item_serializer.is_valid():
                new_individual_item_serializer.save()
                return api_response(
                    is_success=True,
                    error_message=None,
                    status_code=status.HTTP_201_CREATED,
                    result=new_individual_item_serializer.data,
                )
            return api_response(
                is_success=False,
                error_message=new_individual_item_serializer.errors,
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
            #getting id from url
            individual_item_id = kwargs.get('id')

            if not individual_item_id:
                return api_response(
                    is_success=False,
                    error_message="An ID must be provided in the URL to update an individual item.",
                    status_code=status.HTTP_400_BAD_REQUEST,
                    result=None,
                )
            
            existing_individual_item = IndividualItem.objects.get(id=individual_item_id)
            updated_individual_item_serializer = IndividualItemSerializer(instance=existing_individual_item, data=request.data)
            if updated_individual_item_serializer.is_valid():
                updated_individual_item_serializer.save()
                return api_response(
                    is_success=True,
                    error_message=None,
                    status_code=status.HTTP_200_OK,
                    result=updated_individual_item_serializer.data,
                )
            return api_response(
                    is_success=False,
                    error_message=updated_individual_item_serializer.errors,
                    status_code=status.HTTP_400_BAD_REQUEST,
                    result=None,
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
                error_message="An error occurred while updating the individual item. " + str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                result=None,
            )
        
    def delete(self, request, *args, **kwargs):
        try:
            #getting item id from url
            individual_item_id = kwargs.get('id')

            if not individual_item_id:
                return api_response(
                    is_success=False,
                    error_message="An ID must be provided in the url to delete an individual item.",
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
            if 'id' in kwargs:
                supplier = Supplier.objects.get(id=kwargs['id'])
                supplier_serializer = SupplierSerializer(supplier)
                return api_response(
                    is_success=True,
                    error_message=None,
                    status_code=status.HTTP_200_OK,
                    result = supplier_serializer.data,
                )
            else:
                suppliers = Supplier.objects.all()
                supplier_serializer = SupplierSerializer(suppliers, many=True)
                return api_response(
                    is_success=True,
                    error_message=None,
                    status_code=status.HTTP_200_OK,
                    result = supplier_serializer.data,
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
                error_message="An error occurred while fetching suppliers. Please try again later." + str(e),
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
            #getting id from url
            supplier_id = kwargs.get('id')

            if not supplier_id:
                return api_response(
                    is_success=False,
                    error_message="An ID must be provided in the URL to update a supplier.",
                    status_code=status.HTTP_400_BAD_REQUEST,
                    result=None,
                )
            
            existing_supplier = Supplier.objects.get(id=supplier_id)
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
            #getting supplier id from url
            supplier_id = kwargs.get('id')

            if not supplier_id:
                return api_response(
                    is_success=False,
                    error_message="An ID must be provided in the url to delete a supplier.",
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

class TransactionAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            if 'id' in kwargs:
                transaction = Transaction.objects.get(id=kwargs['id'])
                transaction_serializer = TransactionSerializer(transaction)
                return api_response(
                    is_success=True,
                    error_message=None,
                    status_code=status.HTTP_200_OK,
                    result=transaction_serializer.data,
                )
            else:
                transactions = Transaction.objects.all()
                transaction_serializer = TransactionSerializer(transactions, many=True)
                return api_response(
                    is_success=True,
                    error_message=None,
                    status_code=status.HTTP_200_OK,
                    result=transaction_serializer.data,
                )
            
        except Transaction.DoesNotExist:
            return api_response(
                is_success=False,
                error_message="The transaction does not exist.",
                status_code=status.HTTP_404_NOT_FOUND,
                result=None,
            )
        
        except Exception as e:
            return api_response(
                is_success=False,
                error_message="An error occurred while fetching transactions. Please try again later." + str(e),
                status_code=status.HTTP_400_BAD_REQUEST,
                result=None,
            )

    def post(self, request, *args, **kwargs):
        try:
            new_transaction = request.data
            new_transaction_serializer = TransactionSerializer(data=new_transaction)
            if new_transaction_serializer.is_valid():
                new_transaction_serializer.save()
                return api_response(
                    is_success=True,
                    error_message=None,
                    status_code=status.HTTP_201_CREATED,
                    result=new_transaction_serializer.data,
                )
            return api_response(
                is_success=False,
                error_message=new_transaction_serializer.errors,
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
            #getting id from url
            transaction_id = kwargs.get('id')

            if not transaction_id:
                return api_response(
                    is_success=False,
                    error_message="An ID must be provided in the URL to update a transaction.",
                    status_code=status.HTTP_400_BAD_REQUEST,
                    result=None,
                )
            
            existing_transaction = Transaction.objects.get(id=transaction_id)
            updated_transaction_serializer = TransactionSerializer(instance=existing_transaction, data=request.data)
            if updated_transaction_serializer.is_valid():
                updated_transaction_serializer.save()
                return api_response(
                    is_success=True,
                    error_message=None,
                    status_code=status.HTTP_200_OK,
                    result=updated_transaction_serializer.data,
                )
            return api_response(
                    is_success=False,
                    error_message=updated_transaction_serializer.errors,
                    status_code=status.HTTP_400_BAD_REQUEST,
                    result=None,
                )

        except Transaction.DoesNotExist:
            return api_response(
                is_success=False,
                error_message="The transaction does not exist.",
                status_code=status.HTTP_404_NOT_FOUND,
                result=None,
            )
        
        except Exception as e:
            return api_response(
                is_success=False,
                error_message="An error occurred while updating the transaction. " + str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                result=None,
            )
        
    def delete(self, request, *args, **kwargs):
        try:
            #getting transaction id from url
            transaction_id = kwargs.get('id')

            if not transaction_id:
                return api_response(
                    is_success=False,
                    error_message="An ID must be provided in the url to delete a transaction.",
                    status_code=status.HTTP_400_BAD_REQUEST,
                    result=None
                )
            
            deleted_transaction = Transaction.objects.get(id=transaction_id)
            deleted_transaction.delete()

            return api_response(
                is_success=True,
                error_message=None,
                status_code=status.HTTP_204_NO_CONTENT,
                result="Transaction deleted successfully.",
            )
        
        except Transaction.DoesNotExist:
            return api_response(
                is_success=False,
                error_message="The transaction does not exist.",
                status_code=status.HTTP_404_NOT_FOUND,
                result=None,
            )
        
        except Exception as e:
            return api_response(
                is_success=False,
                error_message="An error occurred while deleting the transaction. " + str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                result=None,
            )

class ProjectAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            if 'id' in kwargs:
                project = Project.objects.get(id=kwargs['id'])
                project_serializer = ProjectSerializer(project)
                return api_response(
                    is_success=True,
                    error_message=None,
                    status_code=status.HTTP_200_OK,
                    result=project_serializer.data,
                )
            else:
                projects = Project.objects.all()
                project_serializer = ProjectSerializer(projects, many=True)
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
            new_project_serializer = ProjectSerializer(new_project)
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
            #getting project id from url
            project_id = kwargs.get('id')
            if not project_id:
                return api_response(
                    is_success=False,
                    error_message="An ID must be provided in the URL to update a project.",
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
            project_id = kwargs.get('id')

            if not project_id:
                return api_response(
                is_success=False,
                error_message="An ID must be provided in the url to delete a project.",
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