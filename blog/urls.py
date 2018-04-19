from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    url(r'^tags/(?P<pk>\d+)/$', views.post_tag_list, name='post_tag_list'),
    url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^post/new/$', views.new_post, name='new_post'),
    url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^post/(?P<pk>[0-9]+)/delete/$', views.post_delete, name='post_delete'),
    url(r'^post/(?P<pk>[0-9]+)/comment/$', views.add_comment_to_post, name='add_comment_to_post'),
    url(r'^post/(?P<pk>[0-9]+)/comment_remove/$', views.comment_remove, name='comment_remove'),
    url(r'^post/(?P<pk>[0-9]+)/comment_approve/$', views.comment_approve, name='comment_approve'),
    url(r'^drafts/$', views.post_draft_list, name='post_draft_list'),
    url(r'^contato/$', views.contato, name='contato'),
    url(r'^obg/$', views.obg, name='obg'),
    url(r'^post/(?P<pk>\d+)/publish/$', views.post_publish, name='post_publish')
]