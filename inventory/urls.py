from django.urls import path
from .views import CategoryCreateView, ItemCreateView

urlpatterns = [
    path('categories/', CategoryCreateView.as_view(), name='Category_list'),
    path('items/', ItemCreateView.as_view(), name='items_list'),
]