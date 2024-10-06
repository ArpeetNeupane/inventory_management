from rest_framework import serializers
from .models import Categories, Items

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'

    def validate_name(self, value):
        if Categories.objects.filter(category_name=value).exists():
            raise serializers.ValidationError("Category with this name already exists. Add to existing value instead?")
        return value
    
class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Items
        fields = '__all__'

    def validate_name(self, value):
        if Items.objects.filter(item_name=value).exists():
            raise serializers.ValidationError("Category with this name already exists. Add to existing value instead?")
        return value