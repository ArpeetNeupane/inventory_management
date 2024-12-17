from django.shortcuts import HttpResponse
from inventory_management.utils import api_response

from inventory.models import Item, Category, Transaction
from inventory.serializers import ItemSerializer, CategorySerializer, TransactionSerializer

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView

@api_view(['GET', 'POST'])
def items(request):
    if request.method == 'GET':
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
                error_message=str(e),
                status_code=status.HTTP_400_BAD_REQUEST,
                result=None,
            )
        
    if request.method == 'POST':
        try:
            new_item = request.data
            new_item_serializer = ItemSerializer(data=new_item)
            if new_item_serializer.is_valid():
                new_item_serializer.save()
                return api_response(
                    is_success=True,
                    error_message=None,
                    status_code=status.HTTP_201_CREATED,
                    result = new_item_serializer.data,
                )
            return api_response(
                is_success=False,
                error_message=new_item_serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
                result = None,
            )
        
        except Exception as e:
            return api_response(
                is_success=False,
                error_message=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                result = None,
            )

@api_view(['GET','POST'])
def categories(request):
    if request.method == 'GET':
        try:
            categories = Category.objects.all()
            category_serializer = CategorySerializer(categories, many=True)
            return api_response(
                is_success=True,
                error_message=None,
                status_code=status.HTTP_200_OK,
                result = category_serializer.data,
            )

        except Exception as e:
            return api_response(
                is_success=False,
                error_message=str(e),
                status_code=status.HTTP_400_BAD_REQUEST,
                result=None,
            )
        
    if request.method == 'POST':
        try:
            new_category = request.data
            new_category_serializer = CategorySerializer(data=new_category)
            if new_category_serializer.is_valid():
                new_category_serializer.save()
                return api_response(
                    is_success=True,
                    error_message=None,
                    status_code=status.HTTP_201_CREATED,
                    result = new_category_serializer.data,
                )
            return api_response(
                is_success=False,
                error_message=new_category_serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
                result = None,
            )
        
        except Exception as e:
            return api_response(
                is_success=False,
                error_message=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                result = None,
            )

def individual_items(request):
    return HttpResponse("Individual Item 1 is Raspberry Pi.")

def suppliers(request):
    return HttpResponse("Supplier 1 is Raspberry Pi.")

@api_view(['GET','POST'])
def transactions(request):
    if request.method == 'GET':
        try:
            transactions = Transaction.objects.all()
            transactions_serializer = TransactionSerializer(transactions, many=True)
            return api_response(
                is_success=True,
                error_message=None,
                status_code=status.HTTP_200_OK,
                result = transactions_serializer.data,
            )

        except Exception as e:
            return api_response(
                is_success=False,
                error_message=str(e),
                status_code=status.HTTP_400_BAD_REQUEST,
                result=None,
            )
        
    if request.method == 'POST':
        try:
            new_transaction = request.data
            new_transaction_serializer = TransactionSerializer(data=new_transaction)
            if new_transaction_serializer.is_valid():
                new_transaction_serializer.save()
                return api_response(
                    is_success=True,
                    error_message=None,
                    status_code=status.HTTP_201_CREATED,
                    result = new_transaction_serializer.data,
                )
            return api_response(
                is_success=False,
                error_message=new_transaction_serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
                result = None,
            )
        
        except Exception as e:
            return api_response(
                is_success=False,
                error_message=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                result = None,
            )

def projects(request):
    return HttpResponse("Project 1 is Raspberry Pi.")

class ItemSerializer(APIView):
    def get(self, request, *args, **kwargs):
        try:
            items = Item.objects.all()
            item_serializer = ItemSerializer(items, many=True)
        except:
            pass
    def post(self, request, *args, **kwargs):
        pass