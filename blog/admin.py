from django.contrib import admin
from .models import Post, Categories, PostComment, Videos

# Register your models here.
admin.site.register(Post)
admin.site.register(PostComment)
admin.site.register(Categories)
admin.site.register(Videos)