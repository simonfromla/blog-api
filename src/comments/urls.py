from django.conf.urls import url
from django.contrib import admin

from .views import (
    # post_list,
    # post_create,
    # post_detail,
    # post_update,
    comment_delete,
    comment_thread,
    )

urlpatterns = [
    #url(r'^$', post_list, name='list'),
    # url(r'^create/$', post_create),
    url(r'^(?P<id>\d+)/$', comment_thread, name='thread'),
    # url(r'^(?P<slug>[\w-]+)/edit/$', post_update, name='update'),
    url(r'^(?P<id>\d+)/delete/$', comment_delete, name='delete'),
    #url(r'^posts/$', "<appname>.views.<function_name>"),
]
