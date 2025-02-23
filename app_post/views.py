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



# def home(request): # post_list for all user
#     posts = Post.objects.all().order_by('-created_at')
    
#     context = {
#         'posts': posts,
#         }

#     return render(request, 'app_post/home.html',  context)


from django.db.models import Q

def home(request):  
    posts = Post.objects.all()

    # Get filter parameters from request
    search_query = request.GET.get('q', '')
    sort_order = request.GET.get('sort', '-created_at')  # Default: Newest first
    media_filter = request.GET.get('media', 'all')
    user_filter = request.GET.get('user', '')

    # Search by keyword (use the correct field)
    if search_query:
        posts = posts.filter(Q(title__icontains=search_query) | Q(caption__icontains=search_query))  

    # Sort by date
    if sort_order == 'oldest':
        posts = posts.order_by('created_at')
    else:
        posts = posts.order_by('-created_at')

    # Filter by media type
    if media_filter == 'text-only':
        posts = posts.filter(image='')  # Assuming `image` is a field in your model
    elif media_filter == 'images':
        posts = posts.exclude(image='')

    # Filter by user
    if user_filter:
        posts = posts.filter(author__username=user_filter)

    context = {
        'posts': posts,
        'search_query': search_query,
        'sort_order': sort_order,
        'media_filter': media_filter,
        'user_filter': user_filter,
    }

    return render(request, 'app_post/home.html', context)


@login_required
def my_post(request): # update a post
    posts = Post.objects.all().order_by('-created_at')

     # Get filter parameters from request
    search_query = request.GET.get('q', '')
    sort_order = request.GET.get('sort', '-created_at')  # Default: Newest first
    media_filter = request.GET.get('media', 'all')
    user_filter = request.GET.get('user', '')

    # Search by keyword (use the correct field)
    if search_query:
        posts = posts.filter(Q(title__icontains=search_query) | Q(caption__icontains=search_query))  

    # Sort by date
    if sort_order == 'oldest':
        posts = posts.order_by('created_at')
    else:
        posts = posts.order_by('-created_at')

    # Filter by media type
    if media_filter == 'text-only':
        posts = posts.filter(image='')  # Assuming `image` is a field in your model
    elif media_filter == 'images':
        posts = posts.exclude(image='')

    # Filter by user
    if user_filter:
        posts = posts.filter(author__username=user_filter)

    context = {
        'posts': posts,
        'search_query': search_query,
        'sort_order': sort_order,
        'media_filter': media_filter,
        'user_filter': user_filter,
    }


    
    return render(request, 'app_post/my_post.html',  context)

@login_required
def post_details(request, id):
    posts = Post.objects.filter(id=id).order_by('-created_at')
    # posts = get_object_or_404(Post, id=id)
    context = {
        'posts': posts,    
        }
    
    return render(request, 'app_post/post_deatails.html',  context)


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