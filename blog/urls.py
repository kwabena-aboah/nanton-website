from django.urls import path
from . import views
from .views import home, media, blog, search, CategoryView, blogdetail, contactView, profile


urlpatterns = [
    path('', home, name="home"),
    path('news/', blog.as_view(), name="blog"),
    path('media/', media, name="media"),
    path('search', search, name="search"),
    path('contact/', contactView, name='contact'),
    path('about-us/', profile, name='profile'),
    path('category/<str:cats>/', CategoryView, name="category"),
    path('<slug:slug>/send-comment', views.send_comment, name="send_comment"),
    path('<slug:slug>/', blogdetail.as_view(), name="blog-detail"),
]
