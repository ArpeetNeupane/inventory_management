from django.urls import path
from inventory import views

urlpatterns = [
    path('item/', views.items, name='items_list'),
    path('category/', views.categories, name='items_list'),
    path('individual_item/', views.individual_items, name='items_list'),
    path('supplier/', views.suppliers, name='items_list'),
    path('transaction/', views.transactions, name='items_list'),
    path('project/', views.projects, name='items_list'),
]