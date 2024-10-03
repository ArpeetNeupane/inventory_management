from rest_framework import generics
from .models import Items, Categories
from .serializers import CategorySerializer
from rest_framework.permissions import IsAuthenticated

class CategoryCreateView(generics.ListCreateAPIView):
    queryset = Categories.objects.all()
    serializered_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class ItemCreateView(generics.ListCreateAPIView):
    queryset = Items.objects.all()
    serializered_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)