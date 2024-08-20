from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    return render(request, "home.html", {})

def authView(request):
    if request.method == 'GET':
        # When GET request, render the signup form
        form = UserCreationForm()
        return render(request, 'registration/signup.html', {'form': form}) 

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
