from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import Http404, HttpResponseRedirect
from django.core.mail import send_mail, BadHeaderError
from django.contrib import messages
from .models import Post, Categories, PostComment, Videos
from .forms import ContactForm


# Create your views here.
def home(request):
       latestpost_list = Post.objects.all().order_by('-post_date')[:3]
       cat_list = Categories.objects.all()
       videos = Videos.objects.all().order_by('-post_date')[:1]
       context = {'latestpost_list': latestpost_list, 'cat_list': cat_list, 'videos': videos}
       return render(request, 'blog/index.html', context)
    
    
def media(request):
      latestpost_list = Post.objects.all().order_by('-post_date')[:3]
      cat_list = Categories.objects.all()
      videos = Videos.objects.all().order_by('-post_date')[:3]
      context = {'latestpost_list': latestpost_list, 'cat_list': cat_list, 'videos': videos}
      return render(request, 'blog/media.html', context)


def profile(request):
      latestpost_list = Post.objects.all().order_by('-post_date')[:3]
      cat_list = Categories.objects.all()
      context = {'latestpost_list': latestpost_list, 'cat_list': cat_list}
      return render(request, 'blog/profile.html', context)
       
class blog(ListView):
   model = Post
   template_name = 'blog/blog_list.html'
   context_object_name = 'posts'
   cats = Categories.objects.all()
   ordering = ['-post_date']  
   paginate_by = 10

   def get_context_data(self, *args, **kwargs):
      cat_list = Categories.objects.all()
      latestpost_list = Post.objects.all().order_by('-post_date')[:12]
      context = super(blog, self).get_context_data(*args, **kwargs)
      context["cat_list"] = cat_list
      context["latestpost_list"] = latestpost_list
      return context

def search(request):
   template = 'blog/search_list.html'
   query = request.GET.get('q')
   if query:
      posts = Post.objects.filter(Q(title__icontains=query) | Q(body__icontains=query)).order_by('-post_date')
   else:
      posts = Post.objects.all()
   
   cat_list = Categories.objects.all()
   latestpost_list = Post.objects.all().order_by('-post_date')[:3]
   paginator = Paginator(posts, 2)
   page = request.GET.get('page')
   posts = paginator.get_page(page)
   return render(request, template, {'posts':posts, 'cat_list': cat_list, 'latestpost_list':latestpost_list, 'query':query})

def CategoryView(request, cats):
   if Categories.objects.filter(categoryname=cats).exists():
      category_posts = Post.objects.filter(category__categoryname=cats).order_by('-post_date')
      cat_list = Categories.objects.all()
      latestpost_list = Post.objects.all().order_by('-post_date')[:3]
      paginator = Paginator(category_posts, 2)
      page = request.GET.get('page')
      category_posts = paginator.get_page(page)
      return render(request, 'blog/category_list.html', {'cats':cats, 'category_posts':category_posts, 'cat_list': cat_list, 'latestpost_list':latestpost_list})
   else:
      raise Http404

class blogdetail(DetailView):
   model = Post
   template_name = 'blog/blog_detail.html'

   def get_context_data(self, *args, **kwargs):
      cat_list = Categories.objects.all()
      latestpost_list = Post.objects.all().order_by('-post_date')[:3]
      context = super(blogdetail, self).get_context_data(*args, **kwargs)
      context["cat_list"] = cat_list
      context["latestpost_list"] = latestpost_list
      return context

@login_required(login_url='/login')
def send_comment(request, slug):
   message = request.POST.get('message')
   post_id = request.POST.get('post_id')
   post_comment = PostComment.objects.create(sender=request.user, message=message)
   post = Post.objects.filter(id=post_id).first()
   post.comments.add(post_comment)
   return redirect('.')


def contactView(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email, ['admin@example.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            messages.info(request, 'Success! Thank you for your message.')
            return HttpResponseRedirect('/contact')
    return render(request, "blog/contact.html", {'form': form})