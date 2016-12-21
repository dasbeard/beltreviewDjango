from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add$', views.add, name='add'),
    url(r'^(?P<id>\d+)$', views.book, name='book'),
    url(r'^user/(?P<id>\d+)$', views.user, name='user'),
    url(r'^create_review/(?P<id>\d+)$', views.create_review, name='create_review'),
    url(r'^create_book$', views.create_book, name='create_book'),
    url(r'^delete/(?P<id>\d+)$', views.delete, name='delete'),

]
