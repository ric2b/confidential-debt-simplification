from django.conf.urls import url
from . import views

app_name = 'main_server_app'
urlpatterns = [
    url(r'^issue-uome/$', views.issue_uome, name='issue_uome'),
    url(r'^cancel-uome/$', views.cancel_uome, name='cancel_uome'),
    url(r'^get_unconfirmed_uomes/$', views.get_unconfirmed_uomes, name='get_unconfirmed_uomes'),
    url(r'^confirm-uome/$', views.confirm_uome, name='confirm_uome'),
    url(r'^total-debt/$', views.get_total_debt, name='total_debt'),
    url(r'^register-group/$', views.register_group, name='register_group'),
    url(r'^join-group/$', views.join_group, name='join-group'),
]
