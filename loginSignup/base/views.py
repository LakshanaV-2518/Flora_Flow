from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.contrib.auth import logout
from django.urls import reverse
from .models import Post
from .forms import PostForm

# View to handle user signup
def authView(request):
    if request.method == "GET":
        form = UserCreationForm()
        return render(request, "registration/signup.html", {"form": form})
    elif request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("base:login")  # Redirect to login after successful signup
        return render(request, "registration/signup.html", {"form": form})
    return HttpResponse("Invalid request method", status=405)

# View to handle the home page, requires login
@login_required
def home(request):
    return render(request, "about.html")

# View to render the "Care Tips" page
def care_tips(request):
    posts = Post.objects.all()
    return render(request, "care_tips.html", {"posts": posts, "user": request.user})


# View to list all posts
def post_list(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 5)  # Show 5 posts per page
    page = request.GET.get('page')
    
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver last page of results
        posts = paginator.page(paginator.num_pages)
    
    return render(request, "blog/post_list.html", {"posts": posts, "user": request.user})
    


# View to create a new post
@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("blog:post_list")
    else:
        form = PostForm()
    return render(request, "blog/post_form.html", {"form": form})


# View to display a single post
def post_view(request, id):
    post = get_object_or_404(Post, id=id)
    form = PostForm(instance=post)
    return render(request, "blog/post_view.html", {"form": form, "user": request.user})


# View to update a post
@login_required
def post_update(request, id):
    post = get_object_or_404(Post, id=id)
    if post.author != request.user and not request.user.is_superuser:
        messages.error(request, "You do not have permission to edit this post.")
        return redirect("blog:post_list")

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect("blog:post_list")
    else:
        form = PostForm(instance=post)
    return render(request, "blog/post_form.html", {"form": form})


# View to delete a post
@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user and not request.user.is_superuser:
        return redirect("blog:post_list")

    if request.method == "POST":
        if "confirm_delete" in request.POST:  # Check if the user clicked the delete button
            post.delete()
            return redirect("blog:post_list")
        else:  # User canceled the deletion
            return redirect("blog:post_list")

    return render(request, "blog/post_confirm_delete.html", {"post": post})


# View to handle sign out
def signout(request):
    if request.method == "POST":
        logout(request)
        return redirect(reverse('login'))  # Redirect to login page after logout