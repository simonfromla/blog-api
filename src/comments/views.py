from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render, get_object_or_404

from .forms import CommentForm
from .models import Comment
# Create your views here.

#By adding this @login_required decorator, if user attempts to reach delete view without logging in,
# will be redirected to login_url. See accounts/views.py/login_view for 'next' steps
@login_required #(login_url='/login/') #LOGIN_URL = '/login/' #Change the default in settings.py
def comment_delete(request, id):
    # obj = get_object_or_404(Comment, id=id)
    # obj = Comment.objects.get(id=id)
    try:
        obj = Comment.objects.get(id=id)
    except:
        raise Http404

# ADD--"if its a child comment youre deleting, redirect to parent thread"
#some security. 403 = standard code regarding permissions
    if obj.user != request.user:
        # messages.success(request, "You do not have permission.")
        # raise Http404
        response = HttpResponse("You do not have permission.")
        response.status_code = 403
        return response

    #if POST clause to add a confirmation page/step before deleting
    #requires them to go to the confirmation template, and submit a blank form with a POST request
    if request.method == "POST":
        # obj being the actual instance, content_object being where it exists(Post), get_abs_url() from Post
        parent_obj_url = obj.content_object.get_absolute_url()
        obj.delete()
        messages.success(request, "Your comment has been deleted")
        return HttpResponseRedirect(parent_obj_url)
    context = {
        "object": obj
    }
    return render(request, "confirm_delete.html", context)

def comment_thread(request, id):
    # obj = get_object_or_404(Comment, id=id)
    # obj = Comment.objects.get(id=id)
    try:
        obj = Comment.objects.get(id=id)
    except:
        raise Http404

# Setting the object to a parent if it is not a parent. Used for allowing deletion of each parent comment
# Also adjusts urls so that when you directly go to a child comment ID's url, will take you to thread with its parent
#ADV22
    if not obj.is_parent:
        obj = obj.parent


    content_object = obj.content_object #samesame: the Post that the comment is on
    content_id = obj.content_object.id

    initial_data = {
        "content_type": obj.content_type,
        "object_id": obj.object_id
    }

    form = CommentForm(request.POST or None, initial=initial_data)

    print(dir(form))
    print(form.errors)

    if form.is_valid() and request.user.is_authenticated():
        c_type = form.cleaned_data.get("content_type")
        content_type = ContentType.objects.get(model=c_type)
        obj_id = form.cleaned_data.get('object_id')
        content_data = form.cleaned_data.get("content")

#parent_id uses request.POST.get instead of .cleaned_data b/c we didn't include into comments/forms.CommentForm
# Avoid a hairy sitch trying to set parent id for each comment in the view. Instead, we set the CommentForm one
# time, with initial_data one time. See above^
# So, add custom safeguards to make sure parent_id exists in DB.
        #Init parent_obj to None since it is used down(v) there. SO, it should stay None all the way thorugh
        # unless all the other checks are passed.
        parent_obj = None
# 1) try/except. Make sure its an Int. If not int and except raises TypeError(?), set to None
        try:
            parent_id = int(request.POST.get('parent_id'))
        except:
            parent_id = None

#2) If parent_id is not None(^) and one is given, then check if that id exists in the DB
        if parent_id:
            # if parent_id, filter it by that id
            parent_qs = Comment.objects.filter(id=parent_id)
            # if filtered qs exists in db, set the first()(there should be only 1 item) item of that qs list to parent_obj
            if parent_qs.exists() and parent_qs.count() == 1:
                parent_obj = parent_qs.first()

            # Finally, create the comment. If its a reply, parent_obj will have a value.
        new_comment, created = Comment.objects.get_or_create(
                            user = request.user,
                            content_type= content_type,
                            object_id = obj_id,
                            content = content_data,
                            parent = parent_obj,
                        )

        #Clearing the comment form after its been submitted:
        #If the form.is_valid, and it's been created, return a redirect
        #new_comment from ^above refers to Comment model, .content_object from inside the Comment model which, in this case,
        # refers to the Post model, and the .get_absolute_url() method in Post returns a new detail page.
        return HttpResponseRedirect(obj.get_absolute_url())

    context = {
        'comment': obj,
        'form': form,
    }
    return render(request, "comment_thread.html", context)