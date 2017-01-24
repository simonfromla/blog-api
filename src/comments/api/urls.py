from django.conf.urls import url
from django.contrib import admin

from .views import (
    CommentDetailAPIView,
    CommentListAPIView,
    )

urlpatterns = [
    url(r'^$', CommentListAPIView.as_view(), name='list'),
    # url(r'^create/$', CommentCreateUpdateAPIView.as_view()),
    url(r'^(?P<pk>\d+)/$', CommentDetailAPIView.as_view(), name='thread'),
#     url(r'^(?P<id>\d+)/delete/$', comment_delete, name='delete'),
]
