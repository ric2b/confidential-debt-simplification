from django.conf.urls import url
from . import views

app_name = 'main_server_app'
urlpatterns = [
#    url(r'^$', views.IndexView.as_view(), name='index'),
#    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
#    url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
#    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    url(r'^add-uome/$', views.add_uome, name='add_uome'),
    url(r'^cancel-uome/$', views.cancel_uome, name='cancel_uome'),
    url(r'^get_unconfirmed_uomes/$', views.get_unconfirmed_uomes, name='get_unconfirmed_uomes'),
    url(r'^confirm-uome/$', views.confirm_uome, name='confirm_uome'),
    url(r'^total-debt/$', views.get_total_debt, name='total_debt'),
    url(r'^register-group/$', views.register_group, name='register_group'),
    url(r'^get-group-info/$', views.get_group_info, name='get_group_info'),
]