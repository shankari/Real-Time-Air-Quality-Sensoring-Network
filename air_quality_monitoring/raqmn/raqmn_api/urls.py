from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^data/(?P<uuid>$)', views.get_data_by_uuid, name='get_data_by_uuid'),
]