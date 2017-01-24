from django.conf.urls import url
from django.contrib import admin

from .views import (
    CommentCreateUpdateAPIView,
    CommentDetailAPIView,
    CommentListAPIView,
    )

urlpatterns = [
    url(r'^$', CommentListAPIView.as_view(), name='list'),
    url(r'^create/$', CommentCreateUpdateAPIView.as_view()),
    url(r'^(?P<id>\d+)/$', CommentDetailAPIView.as_view(), name='thread'),
#     # url(r'^(?P<slug>[\w-]+)/edit/$', post_update, name='update'),
#     url(r'^(?P<id>\d+)/delete/$', comment_delete, name='delete'),
#     #url(r'^posts/$', "<appname>.views.<function_name>"),
]
