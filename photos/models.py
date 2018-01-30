
import uuid
from django.db import models

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

import datetime

class Album(models.Model):
    title = models.CharField(max_length=120)
    #description = models.TextField()
    
    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    image = models.ImageField(upload_to="images", height_field='height', width_field='width')
    thumb = ImageSpecField(source='image', processors=[ResizeToFill(350, 350)])
    
    date = models.DateField(default=datetime.date(1994,5,9)) 
    slug = models.SlugField(default=uuid.uuid4, editable=False) #exc
    
    def __str__(self):
        return self.title
        
        
class Photo(models.Model):
          
    created = models.DateTimeField(auto_now_add=True)
    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    
    album = models.ForeignKey('album', on_delete=models.CASCADE)
    slug = models.SlugField(max_length=70, default=uuid.uuid4, editable=False) 
    
    image = models.ImageField(upload_to="images", height_field='height', width_field='width')
    thumb = ImageSpecField(source='image', processors=[ResizeToFill(250, 250)]) # these are all stored in  'media/CACHE/...'
    
    def __str__(self):
        return "{}".format(self.slug)
    