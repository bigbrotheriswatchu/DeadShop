from django.urls import path
from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^collection/(?P<collection_slug>[-\w]+)/$', list_of_tshirts_by_collection, name='list_t_shirts'),
    url(r'^product/(?P<product_id>\w+)/$', product, name='product'),
    url(r'^basket_adding/$', basket_adding, name="basket_adding"),
    path('', index, name='home'),
]