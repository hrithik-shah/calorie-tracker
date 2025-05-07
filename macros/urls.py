from django.urls import include, path
from .views import *

urlpatterns = [
    path('api/log/new/', log_new_food, name='log-food-new'),
    path('api/log/existing/', log_existing_food, name='log-food-existing'),
    path('api/get/', get, name='get-foods'),
]