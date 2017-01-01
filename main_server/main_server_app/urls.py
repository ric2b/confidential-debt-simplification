from django.conf.urls import url
from . import views

app_name = 'main_server_app'
urlpatterns = [
    url(r'^issue-uome/$', views.issue_uome, name='issue_uome'),
    url(r'^confirm-uome/$', views.confirm_uome, name='confirm_uome'),
    url(r'^cancel-uome/$', views.cancel_uome, name='cancel_uome'),
    url(r'^get-pending-uomes/$', views.get_pending_uomes, name='get_pending_uomes'),
    url(r'^accept-uome/$', views.accept_uome, name='accept_uome'),
    url(r'^get-totals/$', views.get_totals, name='get_totals'),
    url(r'^register-group/$', views.register_group, name='register_group'),
    url(r'^join-group/$', views.join_group, name='join-group'),
]
