from rest_framework import generics
from .models import Inventory
from .serializers import CategorySerializer

class CategoryCreateView(generics.ListCreateView):
    pass