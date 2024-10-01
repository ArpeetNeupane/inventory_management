from rest_framework import serializers
from .models import Inventory

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ['item']

    def validate_name(self, value):
        if Inventory.objects.filter(item=value).exists():
            raise serializers.ValidationError("Category with this name already exists.")
        return value

     