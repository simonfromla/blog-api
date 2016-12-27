try:
    from urllib import quote_plus #python 2
except:
    pass

try:
    from urllib.parse import quote_plus #python 3
except:
    pass

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from comments.forms import CommentForm
from comments.models import Comment
from .forms import PostForm
from .models import Post
# from .utils import get_read_time

def post_create(request):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404

	form = PostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.user = request.user
		instance.save()
		# message success
		messages.success(request, "Successfully Created")
		return HttpResponseRedirect(instance.get_absolute_url())
	context = {
		"form": form,
	}
	return render(request, "post_form.html", context)

def post_detail(request, slug=None):
	instance = get_object_or_404(Post, slug=slug)
	if instance.publish > timezone.now().date() or instance.draft:
		if not request.user.is_staff or not request.user.is_superuser:
			raise Http404
	share_string = quote_plus(instance.content)


#Init Comment GFK, query, and send to template
			#specify which content_type you want (Post)
	#content_type = ContentType.objects.get_for_model(Post)
			#specify which exact post, by associating with a Post instance's id (similar to Post.objects.get(id=instance.id))
	#obj_id = instance.id
			#Now that we have information to narrow down to a specific instance of a content_type, use both
	# to query, filter, and then add to the context.
	#comments = Comment.objects.filter(content_type=content_type, object_id=obj_id)
			#^this will give us a LIST of the comments related to the object_id(obj.id)
			#SO, go into post_detail.html and iterate through them to retrieve individual comments
	#!!! commented out this^ GFK method for use of another. See below:


			#The NEWer method below makes use of a modelManager
			# **instance method < > queryset method
	comments = instance.comments #Comment.objects.filter_by_instance(instance)

#Initial data related to the fields
#See:ADV 15
	initial_data = {
	#first field: content_type--takes from posts/models.py get_c_type property
			"content_type": instance.get_content_type,
			"object_id": instance.id
	}
	#Initialize the comment form, and set initial data
	form = CommentForm(request.POST or None, initial=initial_data)

#validates, then sends back to post_detail page to update the page with a brand spankin new comment.
#See: comments/models.py - Comment model
	if form.is_valid() and request.user.is_authenticated(): #& user.is_auth doesnt allow anonymous user comment to go through. Must follow up this check in the post_detail template by not allowing comment form to be visible if unauth.
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
		return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

	context = {
		"title": instance.title,
		"instance": instance,
		"share_string": share_string,
		"comments":comments,
		"comment_form":form,
	}
	return render(request, "post_detail.html", context)

def post_list(request):
	today = timezone.now().date()
	queryset_list = Post.objects.active() #.order_by("-timestamp")
	if request.user.is_staff or request.user.is_superuser:
		queryset_list = Post.objects.all()

	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
				Q(title__icontains=query)|
				Q(content__icontains=query)|
				Q(user__first_name__icontains=query) |
				Q(user__last_name__icontains=query)
				).distinct()
	paginator = Paginator(queryset_list, 8) # Show 25 contacts per page
	page_request_var = "page"
	page = request.GET.get(page_request_var)
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		queryset = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		queryset = paginator.page(paginator.num_pages)


	context = {
		"object_list": queryset,
		"title": "List",
		"page_request_var": page_request_var,
		"today": today,
	}
	return render(request, "post_list.html", context)





def post_update(request, slug=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(Post, slug=slug)
	form = PostForm(request.POST or None, request.FILES or None, instance=instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		messages.success(request, "<a href='#'>Item</a> Saved", extra_tags='html_safe')
		return HttpResponseRedirect(instance.get_absolute_url())

	context = {
		"title": instance.title,
		"instance": instance,
		"form":form,
	}
	return render(request, "post_form.html", context)


@login_required
def post_delete(request, slug=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(Post, slug=slug)
	instance.delete()
	messages.success(request, "Successfully deleted")
	return redirect("posts:list")
