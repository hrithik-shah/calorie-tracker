from rest_framework import serializers
from ..models.item import Item

from typing import override

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'
        extra_kwargs = {
            'food': {'read_only': True}
        }

    
    @override
    def create(self, validated_data):
        food = self.context.get('food')
        if food:
            validated_data['food'] = food

        return super().create(validated_data)