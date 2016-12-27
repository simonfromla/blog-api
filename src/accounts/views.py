from django.shortcuts import render, redirect
from django.contrib.auth import(
    authenticate,
    get_user_model,
    login,
    logout)
from .forms import UserLoginForm, UserRegisterForm

# Started off thinking about/defining the basic views needed
# Identify the need for a form in this app
# Created the UserLoginForm in forms.py
# Import the form into the views--(from here, can go straight to importing/adding the view into the urls)
# Updated the login_view with basic validation, and configured its "render"
# Created a basic template, form.html, corresponding to the render function
# Import the views into blog/urls.py and create the corresponding urls

#logout_view doesnt require much logic--just implement the function and
# configure the logout url pattern


def login_view(request):
    print(request.user.is_authenticated())

    #If user is redirected to this page as a result of login_required decorator, the URL will show the
    # GET request with 'next' parameter. Store the next value into the variable 'next' here, and redirect
    # the user to the intended URL upon login completion/authentication.
    next = request.GET.get('next')

    form = UserLoginForm(request.POST or None)
    title = "Login"

    #!!! AS SOON as .is_valid() is called, UserLoginForm's clean method will run and
    # run validation checks. (See: UserLoginForm.clean) If all good, .clean() returns the default data which signifies
    # that data is clean, places the data in the cleaned_data attribute, and *causes* the is_valid() method to return True.
    #After being returned True in this view, we return to this view, do a couple redundant checks in order to
    # get the data, and then Log In the user using the imported login function.
    if form.is_valid():
        #the "strings" here are a reference to the field names of the form.
        # The submitted POST data in particular.
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")


        user = authenticate(username=username, password=password)
        login(request, user)

        print(request.user.is_authenticated())

        #If user arrived at login page due to login decorator, redirect to the originally intended 'next' page.
        if next:
            return redirect(next)

        # After logging the user in, redirect to the index: "/"
        return redirect("/")
    context = {
    "title":title,
    "form":form
    }
    return render(request, "form.html", context)

def register_view(request):
    print(request.user.is_authenticated())
    next = request.GET.get('next')
    title = "Register"
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')

        #Use built-in .set_password function and pass in the cleaned_data pw
        user.set_password(password)
        #Save the new user
        user.save()
        #Cannot direcly login user--Must authenticate the newly created user
        # before logging in
        new_user = authenticate(username=user.username, password=password)
        #Use built-in login function
        login(request, new_user)
        if next:
            return redirect(next)
        return redirect("/")

    context = {
        "form": form,
        "title": title
    }
    return render(request, "form.html", context)

def logout_view(request):
    #Use the imported logout function, and then add it to the url patterns
    logout(request)
    return redirect("/")