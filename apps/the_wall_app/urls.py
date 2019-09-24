from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^wall$', views.wall),
    url(r'^wall_render$', views.wall_render),
]
