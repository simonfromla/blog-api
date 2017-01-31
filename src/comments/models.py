from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Post no longer needed due to using instance.__class__
#from posts.models import Post


#This Comment model together with the model Manager, allows us to access comments--for ANY content type.
# This is done by way of separation of concerns, loose coupling, added flexibility, etc. thanks to GFK.
# This app/model belongs to no particular other app. For ONE way of usage, it can be made into a method in any other
# class--as is the case in our: posts/models.py--Post model--the only other place it(Comment) is DIRECTLY mentioned in/invoked from.

#ModelManager(filter) for comments using content_type and id
#uses instance.__class__ for loose coupling--comment to be used in any content_type
class CommentManager(models.Manager):
    def filter_by_instance(self, instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        obj_id = instance.id
        qs = super(CommentManager, self).filter(content_type=content_type, object_id= obj_id).filter(parent=None)
        return qs

#may be unnecessary. Adding the .filter(parent=None) to the above comment managager achieves same feat(?)
    def all(self):
        qs = super(CommentManager, self).filter(parent=None)
        return qs

    def create_by_model_type(self, model_type, slug, content, user, parent_obj=None):
        model_qs = ContentType.objects.filter(model=model_type)
        if model_qs.exists():
            SomeModel = model_qs.first().model_class()
            obj_qs = SomeModel.objects.filter(slug=slug)
            if obj_qs.exists() and obj_qs.count() == 1:
                instance = self.model()
                instance.content = content
                instance.user = user
                instance.content_type = model_qs.first()
                instance.object_id = obj_qs.first().id
                if parent_obj:
                    instance.parent = parent_obj
                instance.save()
                return instance
        return None


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)

    #Initial comment method(Template method) below: associates a Comment instance with an instance of a particular Post
    # by using Post as a foreign key--VS the generic foreign key method which allows us to associate a Comment
    # instance with a GFK, allowing us to apply the 'concept' of a comment anywhere(other content
    # types). See: loose coupling
    # post            = models.ForeignKey(Post)



    # GFK comment---
    # Using GFK, the data is here, & logic is now in the View. See: views.post_detail

    #content_type is the actual foreign key
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    #object_id provides id information for finding a particular object
    object_id = models.PositiveIntegerField()
    #content_object IS the GFK object--which uses the above two to find the specific instance
    #See: *comment: use of content_object in post_detail.html
    content_object = GenericForeignKey('content_type', 'object_id')

#We include this field into the model bc we want to be able to reference it inside an instance itself
# Which means, we're going to want to have an instance method. See children below:
    parent = models.ForeignKey("self", null=True, blank=True)

    content         = models.TextField()
    timestamp       = models.DateTimeField(auto_now_add=True)


    objects = CommentManager()

    class Meta:
        ordering = ['-timestamp']

    def __unicode__(self):
        return str(self.user.username)

    def __str__(self):
        return str(self.user.username)

    def get_absolute_url(self):
        return reverse("comments:thread", kwargs={"id": self.id})

    def get_delete_url(self):
        return reverse("comments:delete", kwargs={"id": self.id})


#children=all of the children replies
    def children(self):
        return Comment.objects.filter(parent=self)


    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True