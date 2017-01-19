from django.conf.urls import url
from django.contrib import admin

from .views import (
    PostListAPIView,
    PostDetailAPIView,
    )

urlpatterns = [
#The empty regex signifies the view to appear once the user directs to *this namespace*
    url(r'^$', PostListAPIView.as_view(), name='list'),
    # url(r'^create/$', post_create),
    url(r'^(?P<abc>[\w-]+)/$', PostDetailAPIView.as_view(), name='detail'),
    # url(r'^(?P<slug>[\w-]+)/edit/$', post_update, name='update'),
    # url(r'^(?P<slug>[\w-]+)/delete/$', post_delete),
    #url(r'^posts/$', "<appname>.views.<function_name>"),
]
