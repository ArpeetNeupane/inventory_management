from rest_framework import generics
from .models import Inventory
from .serializers import CategorySerializer
from rest_framework.permissions import IsAuthenticated

class CategoryCreateView(generics.ListCreateView):
    queryset = Inventory.objects.all()
    serializered_data = CategorySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
        serializer.save()