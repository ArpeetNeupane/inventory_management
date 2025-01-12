from django.urls import path
from inventory.views import *

urlpatterns = [
    path('item/', ItemAPIView.as_view(), name='items_list'), #list view for all items
    path('category/', CategoryAPIView.as_view(), name='category_list'),
    path('individual_item/', IndividualItemAPIView.as_view(), name='individual_item_list'),
    path('supplier/', SupplierAPIView.as_view(), name='supllier_list'),
    path('supplier/<int:id>/', SupplierItemAPIView.as_view(), name='supllier_detail'),
    path('purchase/', PurchaseAPIView.as_view(), name='purchase_list'),
    path('purchase/<int:id>/', PurchaseItemAPIView.as_view(), name='purchase_detail'),
    path('project/', ProjectAPIView.as_view(), name='project_list'),
    path('project/<int:id>/', ProjectItemAPIView.as_view(), name='project_detail'),
]