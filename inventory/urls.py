from django.urls import path
from inventory.views import ItemAPIView, TransactionAPIView, CategoryAPIView, IndividualItemAPIView, SupplierAPIView, ProjectAPIView

urlpatterns = [
    path('item/', ItemAPIView.as_view(), name='items_list'), #list view for all items
    path('item/<int:id>/', ItemAPIView.as_view(), name='item_detail'), #view for 1 item
    path('category/', CategoryAPIView.as_view(), name='category_list'),
    path('category/<int:id>/', CategoryAPIView.as_view(), name='category_detail'),
    path('individual_item/', IndividualItemAPIView.as_view(), name='individual_item_list'),
    path('individual_item/<int:id>/', IndividualItemAPIView.as_view(), name='individual_item_detail'),
    path('supplier/', SupplierAPIView.as_view(), name='supllier_list'),
    path('supplier/<int:id>/', SupplierAPIView.as_view(), name='supllier_detail'),
    path('transaction/', TransactionAPIView.as_view(), name='transaction_list'),
    path('transaction/<int:id>/', TransactionAPIView.as_view(), name='transaction_detail'),
    path('project/', ProjectAPIView.as_view(), name='project_list'),
    path('project/<int:id>/', ProjectAPIView.as_view(), name='project_detail'),
]