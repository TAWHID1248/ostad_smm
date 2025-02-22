from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from . forms import PostForm
from django.contrib.auth.models import User
# authencations form
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout

# messages 
from django.contrib import messages

# authencations views
from django.contrib.auth.decorators import login_required



def home(request): # post_list for all user
    posts = Post.objects.all().order_by('-created_at')
    
    context = {
        'posts': posts,
        }

    return render(request, 'app_post/home.html',  context)

@login_required
def my_post(request): # update a post
    posts = Post.objects.all().order_by('-created_at')
    context = {
        'posts': posts,    
        }
    
    return render(request, 'app_post/my_post.html',  context)

@login_required
def create_post(request): # create a new post
    # form
    form = PostForm()
    
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            form.save()
            messages.success(request, 'Post created successfully.')
        return redirect('app_post:home')
        
    context = {
        'form': form,    
        }
    
    return render(request, 'app_post/create_post.html',  context)

@login_required
def update_post(request, id): # update a post
    post = get_object_or_404(Post, id=id)
    form = PostForm(instance=post)
    
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.warning(request, 'Post updated successfully.')
        return redirect('app_post:home')
    
    context = {
        'form': form,    
        }
    
    return render(request, 'app_post/update_post.html',  context)


@login_required
def delete_post(request, id): # delete a post
    post = get_object_or_404(Post, id=id)

    # request.user = request.id
    post.delete()
    messages.warning(request, 'Post deleted')
    return redirect('app_post:home')


def sign_up(request):
    form = UserCreationForm()
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('app_post:home')
    
    context = {
        'form': form,    
        }
    
    return render(request, 'registrations/signup.html',  context)



def logout_view(request):
    logout(request)
    
    return redirect('app_post:home')