from django.conf.urls import url, include
from . import views

app_name = 'group_server_app'
urlpatterns = [
    url(r'^invite-user$', views.invite_user, name='invite_user'),
    url(r'^join-group$', views.join_group, name='join_group'),
    url(r'^confirm-join$', views.confirm_join, name='confirm_join'),
    url(r'^email-key-map$', views.email_key_map, name='email_key_map'),
]
