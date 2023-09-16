from django.db import models
from django.contrib.auth.models import User

# Create your models herehttp://127.0.0.1:8000/admin/.
class Post(models.Model):
    title = models.CharField(max_length=200, blank=True)    
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    like = models.ManyToManyField(User, related_name='related_post', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    tag = models.ForeignKey('Tag' , on_delete=models.CASCADE, blank=True, null=True)
    def __str__(self):
        return self.content

class Meta:
    ordering = ["-created_at"]
    
    
class Tag(models.Model):
    name = models.CharField(max_length=10, unique=True, default='')
    def __str__(self):
        return self.name