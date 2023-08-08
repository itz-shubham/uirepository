from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from requests import Request

from .models import Post, User
from .forms import PostUploadForm, PostUploadModelForm

def home(request:Request):
    posts = Post.objects.order_by('-datetime').all()
    paginator = Paginator(posts, 12)
    page_number = request.GET.get('page')
    posts_list = paginator.get_page(page_number)
    return render(request, 'home.html', context={'posts_list': posts_list})


def post(request:Request, post_url:str):
    post = get_object_or_404(Post, url=post_url)

    liked = False if request.user.is_anonymous else post.likes.contains(request.user)

    if(request.method == "POST"):
        if (request.POST['type'] == 'delete'):
            if(post and (post.author == request.user)):
                post.delete()
                return HttpResponse("Deleted Successfully", 200)
            else:
                return HttpResponse("You do not have permission to delete this post", 403)
        elif request.POST['type'] == 'like':
            if request.user.is_anonymous:
                return HttpResponseRedirect(f'/accounts/login')
            elif post and (post.author != request.user):
                if liked:
                    post.likes.remove(request.user) 
                    liked = False
                else:
                    post.likes.add(request.user)
                    liked = True
        
    viewed_posts = request.session.get('viewed_posts', [])
    if post.pk not in viewed_posts:
        post.views += 1
        post.save()
        viewed_posts.append(post.pk)
        request.session['viewed_posts'] = viewed_posts

    return render(request, 'post.html', context={'post':post, 'like_count': post.likes.count(), 'liked': liked})
    

def edit_post(request:Request, post_url:str):
    if request.method == "POST":
        print(request.POST)
        post = get_object_or_404(Post, url=post_url)
        if request.POST['title']:
            post.title = request.POST['title']
        if request.FILES and request.FILES['post_image']:
            post.post_image = request.FILES['post_image']
        if request.POST['content']:
            post.content = request.POST['content']
        if request.POST['tech_stack']:
            post.tech_stack = request.POST['tech_stack']
        post.save()
        return HttpResponseRedirect(f'/post/{post.url}')

    post = Post.objects.filter(url=post_url).first()
    form = PostUploadModelForm(instance=post)
    return render(request, 'upload.html', context={'form':form})


def search(request):
    query = request.GET.get('q')
    if query:
        results = Post.objects.filter(title__icontains=query)
        return render(request, 'search_results.html', {'results': results, 'query': query})
    else:
        return HttpResponseRedirect('/')


@login_required
def upload(request:Request):
    if request.method == "POST":
        form = PostUploadForm(request.POST, request.FILES)
        if form.is_valid():
            post = Post(
                title = form.cleaned_data['title'],
                post_image = form.cleaned_data['post_image'],
                content = form.cleaned_data['content'],
                author = request.user,
                tech_stack = form.cleaned_data['tech_stack'],
            )
            post.save()
            return HttpResponseRedirect(f'/post/{post.url}')
    else:
        form = PostUploadForm()

    return render(request, 'upload.html', context={'form': form})


@login_required
def profile(request):
    errors = {}
    if request.method == "POST":
        user:User = request.user
        if(request.FILES and request.FILES['profile_picture']):
            user.profile_picture = request.FILES['profile_picture']
        if(request.POST['first_name']):
            user.first_name = request.POST['first_name']
        if(request.POST['last_name']):
            user.last_name = request.POST['last_name']
        if(request.POST['username'] and (user.username != request.POST['username'])):
            try:
                User.objects.get(username=request.POST['username'])
                errors['username'] = [f"username '{request.POST['username']}' already exists"]
            except User.DoesNotExist:
                user.username = request.POST['username']
        if(request.POST['buymeacoffee']):
            prefix = 'https://www.buymeacoffee.com/'
            if request.POST['buymeacoffee'].startswith(prefix) and len(request.POST['buymeacoffee']) > len(prefix):
                user.buymeacoffee = request.POST['buymeacoffee']
            elif request.POST['buymeacoffee'] == prefix:
                user.buymeacoffee = ''
            else:
                errors['buymeacoffee'] = ['Enter a valid buymeacoffee page link']

        try:
            user.save()
        except Exception as e:
            errors['error_all'] = str(e)

    return render(request, 'profile.html', context={'errors': errors})

