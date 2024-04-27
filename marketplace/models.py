from django.db import models

from accounts.models import User
from menu.models import FoodItem

# Create your models here.

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fooditem = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.fooditem.food_title

    """   #if we want use user as return string will use unicode method because user is foreignkey
    def __unicode__(self):
            return self.fooditem
    """