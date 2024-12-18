from django.urls import path
from inventory.views import ItemAPIView, TransactionAPIView, CategoryAPIView, IndividualItemAPIView, SupplierAPIView, ProjectAPIView

urlpatterns = [
    path('item/', ItemAPIView.as_view(), name='items_list'),
    path('category/', CategoryAPIView.as_view(), name='items_list'),
    path('individual_item/', IndividualItemAPIView.as_view(), name='items_list'),
    path('supplier/', SupplierAPIView.as_view(), name='items_list'),
    path('transaction/', TransactionAPIView.as_view(), name='items_list'),
    path('project/', ProjectAPIView.as_view(), name='items_list'),
]