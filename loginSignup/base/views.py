from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Post, Flower
from .forms import PostForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

# View to list all posts
def post_list(request):
    posts = Post.objects.all()
    return render(request, "blog/post_list.html", {"posts": posts})


# View to create a new post
@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
             post=form.save(commit=False)
             post.author = request.user
             post.save()
             return redirect("blog:post_list")
    else:
        form = PostForm()
    return render(request, "blog/post_form.html", {"form": form})



def post_view(request, pk):
    post = get_object_or_404(Post, id=pk)
    form = PostForm(instance=post)
    return render(request, "blog/post_view.html", {"form": form})

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
        messages.error(request, "You do not have permission to delete this post.")
        return redirect("blog:post_list")
    
    if request.method == "POST":
        if "confirm_delete" in request.POST:  # Check if the user clicked the delete button
            post.delete()
            messages.success(request, f'The post "{post.title}" was deleted successfully.')
            return redirect("blog:post_list")
        else:  # User canceled the deletion
            messages.info(request, 'Deletion canceled.')
            return redirect("blog:post_list")
    
    return render(request, "blog/post_confirm_delete.html", {"post": post})


# View to handle home page, requires login
@login_required
def home(request):
    return render(request, "about.html")


# View to handle user signup
def authView(request):
    if request.method == "GET":
        # When GET request, render the signup form
        form = UserCreationForm()
        return render(request, "registration/signup.html", {"form": form})
    elif request.method == "POST":
        # Handle POST request (form submission)
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("base:login")  # Redirect to login after successful signup
        # If form is invalid, re-render the form with error messages
        return render(request, "registration/signup.html", {"form": form})
    # Optionally, handle any other methods (though generally not needed)
    return HttpResponse("Invalid request method", status=405)


# View to render the "About" page
def about(request):
    return render(request, "about.html")


# View to render the "Care Tips" page
def care_tips(request):
    return render(request, "care_tips.html")
