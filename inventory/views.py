from django.shortcuts import HttpResponse
from inventory_management.utils import api_response

from inventory.models import Item, Category, IndividualItem, Supplier, Transaction, Project
from inventory.serializers import ItemSerializer, CategorySerializer, IndividualItemSerializer, SupplierSerializer, TransactionSerializer, ProjectSerializer

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView

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
            updated_item = request.data
            updated_item_serializer = ItemSerializer(instance=updated_item, data=updated_item)
            if updated_item_serializer.is_valid():
                updated_item_serializer.save()
                return api_response(
                    is_success=True,
                    error_message=None,
                    status_code=status.HTTP_201_CREATED,
                    result=updated_item_serializer.data,
                )
            return api_response(
                    is_success=False,
                    error_message=updated_item_serializer.errors,
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

class SupplierAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            suppliers = Supplier.objects.all()
            supplier_serializer = SupplierSerializer(suppliers, many=True)
            return api_response(
                is_success=True,
                error_message=None,
                status_code=status.HTTP_200_OK,
                result = supplier_serializer.data,
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

class TransactionAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            transactions = Transaction.objects.all()
            transactions_serializer = TransactionSerializer(transactions, many=True)
            return api_response(
                is_success=True,
                error_message=None,
                status_code=status.HTTP_200_OK,
                result=transactions_serializer.data,
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

class ProjectAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            projects = Project.objects.all()
            project_serializer = ProjectSerializer(projects, many=True)
            return api_response(
                is_success=True,
                error_message=None,
                status_code=status.HTTP_200_OK,
                result = project_serializer.data,
            )
        
        except Exception as e:
            return api_response(
                is_success=False,
                error_message="An error occurred while fetching projects. Please try again later." + str(e),
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
                is_success=False,
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
