from __future__ import unicode_literals
from django.db import models
from ..login.models import User
import re, bcrypt
import datetime

class TravelManager(models.Manager):
    def validate(self, post_data):
        errors = []
        if len(post_data['destination']) < 1: 
            errors.append("Destination must not be empty!")            
        if len(post_data['plan']) < 1: 
            errors.append("Description must not be empty!")            
        if len(post_data['travel_start']) < 1:
            errors.append("Travel Date From must not be empty!")
        else:
            travel_start = datetime.datetime.strptime(post_data['travel_start'], "%Y-%m-%d")
            if travel_start < datetime.datetime.today():
                errors.append("Travel Date From must be future-dated!")   
        if len(post_data['travel_end']) < 1:
            errors.append("Travel Date To must not be empty!")
        else:
            travel_end = datetime.datetime.strptime(post_data['travel_end'], "%Y-%m-%d")
            if travel_end < travel_start:
                errors.append("Travel Date To should not be before the Travel Date From!")    
        return errors

# When creating a model be sure to make the related names and variables easy words to work with. 
class Travel(models.Model):
    destination = models.CharField(max_length=255)
    travel_start = models.DateField()
    travel_end = models.DateField()
    plan = models.CharField(max_length=255)
    travels = models.ManyToManyField(User, related_name="travelled_by")
    add = models.ForeignKey(User, related_name="added_by")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True)
    objects = TravelManager()