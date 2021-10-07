from django.db import models
from datetime import datetime, date 
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.db.models.base import Model 
from django.db.models.signals import pre_save
from .utils import unique_slug_generator


# Create your models here.
class PostComment(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender.get_username()}'
    
    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"


class Categories(models.Model):
    categoryname = models.CharField(max_length=255)

    def __str__(self):
        return self.categoryname
    
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

class Post(models.Model):
    title = models.CharField(max_length=255)
    title_tag = models.CharField(max_length=255, default='Blog Post')
    slug = models.SlugField(max_length=255, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    img = models.ImageField(upload_to='blog', null=True)
    body = RichTextField(blank=False, null=True)
    comments = models.ManyToManyField(PostComment, blank=True)
    post_date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Categories, null=True, on_delete=models.PROTECT, related_name='category_set')

    def __str__(self):
        return self.title + ' | ' + str(self.author)

def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(slug_generator, sender=Post)

class Videos(models.Model):
    file = models.FileField(upload_to='videos', null=True, blank=True)
    post_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.id)
    
    def handle_uploaded_file(f):
        with open(f.name, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
    
    class Meta:
        verbose_name = 'Video'
        verbose_name_plural = 'Videos'