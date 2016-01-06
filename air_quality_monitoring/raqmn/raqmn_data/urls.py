from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^api_specs/', views.api_specs, name='api_specs'),
]