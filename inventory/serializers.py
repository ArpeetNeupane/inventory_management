from rest_framework import serializers
from .models import Items

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Items
        fields = ['item']

    def validate_name(self, value):
        if Items.objects.filter(item_name=value).exists():
            raise serializers.ValidationError("Category with this name already exists.")
        return value

     