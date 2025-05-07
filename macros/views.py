from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import api_view

from django.db import transaction
from django.db.models import Q
 
from .serializers.food_serializer import FoodSerializer
from .serializers.item_serializer import ItemSerializer
from .serializers.log_serializer import LogSerializer
from .models.log import Log
from .models.food import Food
from .models.item import Item

from dataclasses import dataclass

import datetime
import re


def __get_unique_food_name(name: str) -> str:
        name_id = name.lower()
        food_qs = Food.objects.filter(Q(name_id=name_id) | Q(name_id__startswith=f"{name_id} "))
        existing_name_ids = food_qs.values_list('name_id', flat=True)

        
        pattern = re.compile(rf'^{re.escape(name_id)}(?: (\d+))?$')

        suffixes = [
            int(match.group(1)) for nid in existing_name_ids
            if (match := pattern.match(nid)) and match.group(1)
        ]
        next_suffix = max(suffixes, default=1) + 1

        return f"{name} {next_suffix}" if suffixes or name_id in existing_name_ids else name

@api_view(['POST'])
@transaction.atomic
def log_new_food(request):
    data = request.data
    now = datetime.datetime.now()

    if 'name' not in data or not data['name']:
        raise ValidationError({ 'error': 'name is required' })
    name = data['name'].strip()
    new_name = __get_unique_food_name(name)

    food = Food(name=new_name, name_id=new_name.lower())
    food.save()

    if 'items' not in data:
        raise ValidationError({ 'error': 'items is required' })
    items = data['items']

    for item in items:
        serializer = ItemSerializer(data=item, context={ 'food': food })
        if not serializer.is_valid():
            raise ValidationError({ 'error': serializer.errors })
        
        serializer.save()

    log = Log(food=food, timestamp=now)
    log.save()

    return Response(
        { 'detail': f'Created and logged {new_name} successfully.' }, 
        status=status.HTTP_200_OK
    )

def __get_food(name) -> Food:
     name_id = name.lower()
     food = Food.objects.filter(name_id=name_id).first()
     return food
     

@api_view(['POST'])
@transaction.atomic
def log_existing_food(request):
    data = request.data
    now = datetime.datetime.now()

    if 'name' not in data or not data['name']:
        raise ValidationError({ 'error': 'name is required' })
    name = data['name'].strip()
    
    food = __get_food(name)
    if food is None:
         raise ValidationError({ 'error': f'food {name} does not exist.' })

    log = Log(food=food, timestamp=now)
    log.save()

    return Response(
        { 'detail': f'Logged {name} successfully.' }, 
        status=status.HTTP_200_OK
    )

@api_view(['GET'])
def get(request):
        foods = Food.objects.all()
        items = Item.objects.all()
        logs = Log.objects.all()
        food_data = FoodSerializer(foods, many=True).data
        item_data = ItemSerializer(items, many=True).data
        log_data = LogSerializer(logs, many=True).data
        return Response(
            {
                'foods': food_data,
                'items': item_data,
                'logs': log_data
            },
            status=status.HTTP_200_OK
        )
