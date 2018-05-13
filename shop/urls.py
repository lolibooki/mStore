from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^storage/$', views.storage, name='storage'),
    url(r'^statistic/$', views.statistic, name='statistic'),
    url(r'^product_delete/(?P<id>\d+)/$', views.product_delete, name='product_delete'),
    url(r'^product_edit/(?P<id>\d+)/$', views.product_edit, name='product_edit'),
    url(r'^transaction_delete/(?P<id>\d+)/$', views.transaction_delete, name='transaction_delete'),
    url(r'^transaction_accept/(?P<id>\d+)/$', views.transaction_accept, name='transaction_accept'),
    url(r'^transaction_edit/(?P<id>\d+)/$', views.transaction_edit, name='transaction_edit'),
]